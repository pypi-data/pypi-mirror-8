import inspect
import logging
import os
import unittest
import shutil
import StringIO
import tempfile

import deployer
from deployer.config import ConfigStack


TEST_OFFLINE = ("DEB_BUILD_ARCH" in os.environ or "TEST_OFFLINE" in os.environ)


class Base(unittest.TestCase):

    test_data_dir = os.path.join(
        os.path.dirname(inspect.getabsfile(deployer)), "tests", "test_data")

    def get_named_deployment(self, file_name, stack_name):
        """ Get deployment from test_data file.
        """
        return ConfigStack(
            [os.path.join(
                self.test_data_dir, file_name)]).get(stack_name)

    def capture_logging(self, name="", level=logging.INFO,
                        log_file=None, formatter=None):
        if log_file is None:
            log_file = StringIO.StringIO()
        log_handler = logging.StreamHandler(log_file)
        if formatter:
            log_handler.setFormatter(formatter)
        logger = logging.getLogger(name)
        logger.addHandler(log_handler)
        old_logger_level = logger.level
        logger.setLevel(level)

        @self.addCleanup
        def reset_logging():
            logger.removeHandler(log_handler)
            logger.setLevel(old_logger_level)
        return log_file

    def mkdir(self):
        d = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, d)
        return d

    def change_environment(self, **kw):
        """
        """
        original_environ = dict(os.environ)

        @self.addCleanup
        def cleanup_env():
            os.environ.clear()
            os.environ.update(original_environ)

        os.environ.update(kw)
