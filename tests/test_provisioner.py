import inspect
import logging
import os
import unittest
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from prvsnlib.provisioner import Provisioner
from prvsnlib.task import Task
from prvsnlib.queue import Queue
from prvsnlib.runbook import Runbook

logging.basicConfig(format='%(message)s', level=logging.INFO)


class TestTask(Task):

    def __init__(self,):
        Task.__init__(self)

    def run(self):
        with open('/tmp/qweqewqeqweqewdafasfsfd', 'w') as f:
            f.write('hello')
        return '', ''

def test():
    TestTask()


class TestProvisioner(unittest.TestCase):

    @property
    def file(self):
        return '/tmp/qweqewqeqweqewdafasfsfd'

    @property
    def runbook(self):
        this_file = inspect.getfile(inspect.currentframe())
        this_dir = os.path.dirname(os.path.abspath(this_file))
        runbook = os.path.join(this_dir, 'runbook')
        return Runbook('', runbook)

    def setUp(self):
        if os.path.exists(self.file):
            os.unlink(self.file)

    def testProvisioner(self):

        q = Queue()
        TestTask.setQueue(q)

        self.assertFalse(os.path.exists(self.file), 'file should not exist; test set up incorrectly?')

        p = Provisioner(
            self.runbook,
            ['provisioner'],
            queue=q,
            extra_imports={'tests.test_provisioner': ['test']}
        )
        self.assertFalse(os.path.exists(self.file), 'cond should be false; cond changed before task is run?')

        p.run()
        self.assertTrue(os.path.exists(self.file), 'file should exist; cond not changed correctly in task run?')

    def testQueues(self):
        q = Queue()
        TestTask.setQueue(q)
        self.assertEqual(len(q), 0)

        p = Provisioner(
            self.runbook,
            ['queue'],
            queue=q,
            extra_imports={'tests.test_provisioner': ['test']}
        ).run()

        self.assertEqual(len(q), 2)