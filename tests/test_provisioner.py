import inspect
import logging
import os
import unittest
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from prvsnlib.provisioner import Provisioner
from prvsnlib.task import Task
from prvsnlib.queue import Queue

logging.basicConfig(format='%(message)s', level=logging.INFO)

cond = False


class TestTask(Task):

    def __init__(self, t):
        Task.__init__(self)
        self._t = t

    def run(self):
        global cond
        cond = self._t
        return '', ''

def test(t):
    TestTask(t)


class TestProvisioner(unittest.TestCase):

    def runbook(self):
        this_file = inspect.getfile(inspect.currentframe())
        this_dir = os.path.dirname(os.path.abspath(this_file))
        runbook = os.path.join(this_dir, 'runbook')
        return runbook

    def setUp(self):
        pass

    def testProvisioner(self):

        q = Queue()
        TestTask.setQueue(q)

        self.assertFalse(cond, 'cond should be false; test set up incorrectly?')

        p = Provisioner(
            self.runbook(),
            ['provisioner'],
            queue=q,
            extra_imports={'tests.test_provisioner': ['test']}
        )
        self.assertFalse(cond, 'cond should be false; cond changed before task is run?')

        p.run()
        self.assertEqual(cond, 'hello', 'cond should be "hello"; cond not changed correctly in task run?')

    def testQueues(self):
        q = Queue()
        TestTask.setQueue(q)
        self.assertEqual(len(q), 0)

        p = Provisioner(
            self.runbook(),
            ['queue'],
            queue=q,
            extra_imports={'tests.test_provisioner': ['test']}
        ).run()

        self.assertEqual(len(q), 2)