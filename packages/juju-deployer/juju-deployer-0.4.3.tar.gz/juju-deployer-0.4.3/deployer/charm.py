import logging
import os
import urllib2
import shutil

from .vcs import Git, Bzr
from .utils import (
    _check_call,
    _get_juju_home,
    extract_zip,
    get_qualified_charm_url,
    path_join,
    path_exists,
    STORE_URL,
    temp_file,
    yaml_load)


class Charm(object):

    log = logging.getLogger('deployer.charm')

    def __init__(self, name, path, branch, rev, build, charm_url=""):
        self.name = name
        self._path = path
        self.branch = branch
        self.rev = rev
        self._charm_url = charm_url
        self._build = build
        self.vcs = self.get_vcs()

    def get_vcs(self):
        if not self.branch:
            return None
        if self.branch.startswith('git') or 'github.com' in self.branch or \
                os.path.exists(os.path.join(self.branch, '.git')):
            return Git(self.path, self.branch, self.log)
        elif self.branch.startswith("bzr") or self.branch.startswith('lp:') \
                or os.path.exists(os.path.join(self.branch, '.bzr')) \
                or self.branch.startswith('file:'):
            return Bzr(self.path, self.branch, self.log)
        raise ValueError(
            "Could not determine vcs backend for %s" % self.branch)

    @classmethod
    def from_service(cls, name, repo_path, deploy_series, data):
        """
        name: service name
        data['charm']: charm name or store charm url
        data['charm_url'] store charm url
        """
        branch, rev, series = None, None, None
        charm_branch = data.get('branch')
        if charm_branch is not None:
            branch, sep, rev = charm_branch.partition('@')

        charm_path, store_url, build = None, None, None
        name = data.get('charm', name)
        if name.startswith('cs:'):
            store_url = name
        elif name.startswith('local:'):
            # Support vcs charms specifying their
            parts = name[len('local:'):].split('/')
            if len(parts) == 2:
                series, name = parts
            elif data.get('series'):
                series = data['series']
                name = parts.pop()
            else:
                series = deploy_series
            charm_path = path_join(repo_path, series, name)
        elif 'series' in data:
            series = data['series']
            charm_path = path_join(repo_path, series, name)
        else:
            charm_path = path_join(repo_path, deploy_series, name)

        if not store_url:
            store_url = data.get('charm_url', None)

        if store_url and branch:
            cls.log.error(
                "Service: %s has both charm url: %s and branch: %s specified",
                name, store_url, branch)
        if not store_url and not branch:
            cls.log.error(
                "Service: %s has neither charm url or branch specified",
                name)
        elif not store_url:
            build = data.get('build', '')

        return cls(name, charm_path, branch, rev, build, store_url)

    def is_local(self):
        if self._charm_url:
            if self._charm_url.startswith('cs:'):
                return False
        return True

    def exists(self):
        return self.is_local() and path_exists(self.path)

    def is_subordinate(self):
        return self.metadata.get('subordinate', False)

    @property
    def charm_url(self):
        if self._charm_url:
            return self._charm_url
        series = os.path.basename(os.path.dirname(self.path))
        charm_name = self.metadata['name']
        return "local:%s/%s" % (series, charm_name)

    def build(self):
        if not self._build:
            return
        self.log.debug("Building charm %s with %s", self.path, self._build)
        _check_call([self._build], self.log,
                    "Charm build failed %s @ %s", self._build, self.path,
                    cwd=self.path)

    def fetch(self):
        if self._charm_url:
            self._fetch_store_charm()
            return
        elif not self.branch:
            self.log.warning("Invalid charm specification %s", self.name)
            return
        self.log.debug(" Branching charm %s @ %s", self.branch, self.path)
        self.vcs.branch()
        if self.rev:
            self.vcs.update(self.rev)
        self.build()

    @property
    def path(self):
        if not self.is_local() and not self._path:
            self._path = self._get_charm_store_cache()
        return self._path

    @property
    def series_path(self):
        if not self.is_local():
            return None
        return os.path.dirname(self.path)

    def _fetch_store_charm(self, update=False):
        cache_dir = self._get_charm_store_cache()
        self.log.debug("Cache dir %s", cache_dir)

        if os.path.exists(cache_dir) and not update:
            return

        qualified_url = get_qualified_charm_url(self.charm_url)

        self.log.debug("Retrieving store charm %s" % qualified_url)

        if update and os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)

        store_url = "%s/charm/%s" % (STORE_URL, qualified_url[3:])
        with temp_file() as fh:
            ufh = urllib2.urlopen(store_url)
            shutil.copyfileobj(ufh, fh)
            fh.flush()
            extract_zip(fh.name, self.path)
        self.config

    def _get_charm_store_cache(self):
        assert not self.is_local(), "Attempt to get store charm for local"
        # Cache
        jhome = _get_juju_home()
        cache_dir = os.path.join(jhome, ".deployer-store-cache")
        if not os.path.exists(cache_dir):
            os.mkdir(cache_dir)
        return os.path.join(
            cache_dir,
            self.charm_url.replace(':', '_').replace("/", "_"))

    def update(self, build=False):
        if not self.branch:
            return
        assert self.exists()
        self.log.debug(" Updating charm %s from %s", self.path, self.branch)
        self.vcs.update(self.rev)
        if build:
            self.build()

    def is_modified(self):
        if not self.branch:
            return False
        return self.vcs.is_modified()

    @property
    def config(self):
        config_path = path_join(self.path, "config.yaml")
        if not path_exists(config_path):
            return {}

        with open(config_path) as fh:
            return yaml_load(fh.read()).get('options', {})

    @property
    def metadata(self):
        md_path = path_join(self.path, "metadata.yaml")
        if not path_exists(md_path):
            if not path_exists(self.path):
                raise RuntimeError("No charm metadata @ %s", md_path)
        with open(md_path) as fh:
            return yaml_load(fh.read())

    def get_provides(self):
        p = {'juju-info': [{'name': 'juju-info'}]}
        for key, value in self.metadata['provides'].items():
            value['name'] = key
            p.setdefault(value['interface'], []).append(value)
        return p

    def get_requires(self):
        r = {}
        for key, value in self.metadata['requires'].items():
            value['name'] = key
            r.setdefault(value['interface'], []).append(value)
        return r
