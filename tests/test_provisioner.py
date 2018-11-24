import inspect
import logging
import os
import unittest
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from prvsnlib.provisioner import Provisioner
from prvsnlib.runbook import Runbook


def test():
    with open('/tmp/qweqewqeqweqewdafasfsfd', 'w') as f:
        f.write('hello')


class TestProvisioner(unittest.TestCase):

    @property
    def file(self):
        return '/tmp/qweqewqeqweqewdafasfsfd'

    @property
    def runbook(self):
        this_file = inspect.getfile(inspect.currentframe())
        this_dir = os.path.dirname(os.path.abspath(this_file))
        runbook = os.path.join(this_dir, 'runbook')
        return Runbook(runbook)

    def setUp(self):
        if os.path.exists(self.file):
            os.unlink(self.file)

    def testProvisioner(self):

        self.assertFalse(os.path.exists(self.file), 'file should not exist; test set up incorrectly?')

        p = Provisioner(
            self.runbook,
            ['provisioner'],
            extra_imports={'tests.test_provisioner': ['test']},
        )
        self.assertFalse(os.path.exists(self.file), 'cond should be false; cond changed before task is run?')

        p.run()
        self.assertTrue(os.path.exists(self.file), 'file should exist; cond not changed correctly in task run?')


