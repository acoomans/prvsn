import inspect
import os
import unittest

from prvsnlib.runbook import Runbook


class TestRunbook(unittest.TestCase):

    @property
    def runbook(self):
        this_file = inspect.getfile(inspect.currentframe())
        this_dir = os.path.dirname(os.path.abspath(this_file))
        runbook = os.path.join(this_dir, 'runbook')
        return runbook

    @property
    def not_runbook(self):
        return '/tmp/fsdjfhsljfsdhfkqehrklhjkhfdklshjfksahkf'

    def testRunbookRoles(self):
        b = Runbook('runbook', self.runbook)
        self.assertGreater(len(b.roles), 3)

    def testNoRunbook(self):
        b = Runbook('runbook', self.not_runbook)
        self.assertEqual(len(b.roles), 0)

