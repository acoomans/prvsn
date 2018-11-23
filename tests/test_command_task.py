import inspect
import logging
import os
import unittest

from prvsnlib.provisioner import Provisioner
from prvsnlib.runbook import Runbook

logging.basicConfig(format='%(message)s', level=logging.INFO)


class TestCommandTask(unittest.TestCase):

    @property
    def runbook(self):
        this_file = inspect.getfile(inspect.currentframe())
        this_dir = os.path.dirname(os.path.abspath(this_file))
        runbook = os.path.join(this_dir, 'runbook')
        return Runbook(runbook)

    @staticmethod
    def path():
        return '/tmp/fjdhsalfhsajflkashdjfaskfhlsajkfasf'

    def setUp(self):
        if os.path.exists(self.path()):
            os.unlink(self.path())

    def tearDown(self):
        if os.path.exists(self.path()):
            os.unlink(self.path())

    def testBash(self):
        self.assertFalse(os.path.exists(self.path()), 'file should not exist yet; test set up incorrectly?')

        Provisioner(
            self.runbook,
            ['command'],
        ).run()

        self.assertTrue(os.path.exists(self.path()))
