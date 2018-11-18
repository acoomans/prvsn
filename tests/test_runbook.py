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
        return Runbook('', runbook)

    @property
    def not_runbook(self):
        return Runbook('', '/tmp/fsdjfhsljfsdhfkqehrklhjkhfdklshjfksahkf')

    def testRunbookRoles(self):
        self.assertGreater(len(self.runbook.roles), 3)

    def testNoRunbook(self):
        self.assertEqual(len(self.not_runbook.roles), 0)

