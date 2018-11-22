import inspect
import logging
import os
import unittest

from prvsnlib.provisioner import Provisioner
from prvsnlib.runbook import Runbook

logging.basicConfig(format='%(message)s', level=logging.INFO)


class TestFileTask(unittest.TestCase):

    @property
    def runbook(self):
        this_file = inspect.getfile(inspect.currentframe())
        this_dir = os.path.dirname(os.path.abspath(this_file))
        runbook = os.path.join(this_dir, 'runbook')
        return runbook

    @property
    def path1(self):
        return '/tmp/popopopopeqwpeoqpeoqpweoqepoeqpweoq'

    @property
    def path2(self):
        return '/tmp/ewiorqwerqworiuqwporiqwuprequwrqwrr'

    def setUp(self):
        if os.path.exists(self.path1):
            os.unlink(self.path1)
        if os.path.exists(self.path2):
            os.unlink(self.path2)

    def tearDown(self):
        if os.path.exists(self.path1):
            os.unlink(self.path1)
        if os.path.exists(self.path2):
            os.unlink(self.path2)

    def testFile(self):

        self.assertFalse(os.path.exists(self.path1), 'file should not exist yet; test set up incorrectly?')
        self.assertFalse(os.path.exists(self.path2), 'file should not exist yet; test set up incorrectly?')

        Provisioner(
            Runbook('', self.runbook),
            ['file'],
        ).run()

        self.assertTrue(os.path.exists(self.path1), 'file at ' + self.path1 + ' should exist')
        self.assertTrue(os.path.exists(self.path2), 'file at ' + self.path2 + ' should exist')

        with open(self.path2, 'r') as f:
            contents = f.read()
        self.assertEqual(contents, 'ddd\nbbb\nddd\nccc\n')

        os.unlink(self.path1)
        os.unlink(self.path2)
