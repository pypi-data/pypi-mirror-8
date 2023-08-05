import logging
import time

from .base import BaseAction
from ..env import watchers
from ..errors import UnitErrors
from ..utils import ErrorExit


class Importer(BaseAction):

    log = logging.getLogger("deployer.import")

    def __init__(self, env, deployment, options):
        self.options = options
        self.env = env
        self.deployment = deployment

    def add_units(self):
        self.log.debug("Adding units...")
        # Add units to existing services that don't match count.
        env_status = self.env.status()
        reloaded = False

        for svc in self.deployment.get_services():
            cur_units = len(env_status['services'][svc.name].get('units', ()))
            delta = (svc.num_units - cur_units)

            if delta <= 0:
                self.log.debug(
                    " Service %r does not need any more units added.",
                    svc.name)
                continue

            charm = self.deployment.get_charm_for(svc.name)
            if charm.is_subordinate():
                self.log.warning(
                    "Config specifies num units for subordinate: %s",
                    svc.name)
                continue

            self.log.info(
                "Adding %d more units to %s" % (abs(delta), svc.name))
            if svc.unit_placement:
                # Reload status once after non placed services units are done.
                if reloaded is False:
                    # Crappy workaround juju-core api inconsistency
                    time.sleep(5.1)
                    env_status = self.env.status()
                    reloaded = True

                placement = self.deployment.get_unit_placement(svc, env_status)
                for mid in range(cur_units, svc.num_units):
                    self.env.add_unit(svc.name, placement.get(mid))
            else:
                self.env.add_units(svc.name, abs(delta))

    def get_charms(self):
        # Get Charms
        self.log.debug("Getting charms...")
        self.deployment.fetch_charms(
            update=self.options.update_charms,
            no_local_mods=self.options.no_local_mods)

        # Load config overrides/includes and verify rels after we can
        # validate them.
        self.deployment.resolve(self.options.overrides or ())

    def deploy_services(self):
        self.log.info("Deploying services...")
        self.log.debug(self.env)
        env_status = self.env.status()
        reloaded = False

        for svc in self.deployment.get_services():
            if svc.name in env_status['services']:
                self.log.debug(
                    " Service %r already deployed. Skipping" % svc.name)
                continue

            charm = self.deployment.get_charm_for(svc.name)
            self.log.info(
                " Deploying service %s using %s", svc.name, charm.charm_url)

            if svc.unit_placement:
                # We sorted all the non placed services first, so we only
                # need to update status once after we're done with them.
                if not reloaded:
                    self.log.debug(
                        " Refetching status for placement deploys")
                    time.sleep(5.1)
                    env_status = self.env.status()
                    reloaded = True
                num_units = 1
            else:
                num_units = svc.num_units

            placement = self.deployment.get_unit_placement(svc, env_status)

            if charm.is_subordinate():
                num_units = None

            self.env.deploy(
                svc.name,
                charm.charm_url,
                self.deployment.repo_path,
                svc.config,
                svc.constraints,
                num_units,
                placement.get(0))

            if svc.annotations:
                self.log.debug(" Setting annotations")
                self.env.set_annotation(svc.name, svc.annotations)

            if self.options.deploy_delay:
                self.log.debug(" Waiting for deploy delay")
                time.sleep(self.options.deploy_delay)

    def add_relations(self):
        self.log.info("Adding relations...")

        # Relations
        status = self.env.status()
        created = False

        for end_a, end_b in self.deployment.get_relations():
            if self._rel_exists(status, end_a, end_b):
                continue
            self.log.info(" Adding relation %s <-> %s", end_a, end_b)
            self.env.add_relation(end_a, end_b)
            created = True
            # per the original, not sure the use case.
            #self.log.debug(" Waiting 5s before next relation")
            #time.sleep(5)
        return created

    def _rel_exists(self, status, end_a, end_b):
        # Checks for a named relation on one side that matches the local
        # endpoint and remote service.
        (name_a, name_b, rem_a, rem_b) = (end_a, end_b, None, None)

        if ":" in end_a:
            name_a, rem_a = end_a.split(":", 1)
        if ":" in end_b:
            name_b, rem_b = end_b.split(":", 1)

        rels_svc_a = status['services'][name_a].get('relations', {})

        found = False
        for r, related in rels_svc_a.items():
            if name_b in related:
                if rem_a and not r in rem_a:
                    continue
                found = True
                break
        if found:
            return True
        return False

    def check_timeout(self):
        timeout = self.options.timeout - (time.time() - self.start_time)
        if timeout < 0:
            self.log.error("Reached deployment timeout.. exiting")
            raise ErrorExit()
        return timeout

    def wait_for_units(self, ignore_errors=False):
        if self.options.skip_unit_wait:
            return
        timeout = self.check_timeout()
        # Set up the callback to be called in case of unit errors: if
        # ignore_errors is True errors are just logged, otherwise we exit the
        # program.
        if ignore_errors:
            on_errors = watchers.log_on_errors(self.env)
        else:
            on_errors = watchers.exit_on_errors(self.env)
        self.env.wait_for_units(
            int(timeout), watch=self.options.watch,
            services=self.deployment.get_service_names(), on_errors=on_errors)

    def run(self):
        options = self.options
        self.start_time = time.time()

        # Get charms
        self.get_charms()
        if options.branch_only:
            return

        if options.bootstrap:
            self.env.bootstrap()
        self.env.connect()

        self.deploy_services()

        # Workaround api issue in juju-core, where any action takes 5s
        # to be consistent to subsequent watch api interactions, see
        # http://pad.lv/1203105 which will obviate this wait.
        time.sleep(5.1)
        self.add_units()

        ignore_errors = bool(options.retry_count) or options.ignore_errors
        self.log.debug("Waiting for units before adding relations")
        self.wait_for_units(ignore_errors=ignore_errors)

        # Reset our environment connection, as it may grow stale during
        # the watch (we're using a sync client so not responding to pings
        # unless actively using the conn).
        self.env.close()
        self.env.connect()

        self.check_timeout()
        rels_created = self.add_relations()

        # Wait for the units to be up before waiting for rel stability.
        if rels_created and not options.skip_unit_wait:
            self.log.debug(
                "Waiting for relation convergence %ds", options.rel_wait)
            time.sleep(options.rel_wait)
            self.wait_for_units(ignore_errors=ignore_errors)

        if options.retry_count:
            self.log.info("Looking for errors to auto-retry")
            self.env.resolve_errors(
                options.retry_count,
                options.timeout - time.time() - self.start_time)

        # Finally expose things
        for svc in self.deployment.get_services():
            if svc.expose:
                self.log.info(" Exposing service %r" % svc.name)
                self.env.expose(svc.name)
