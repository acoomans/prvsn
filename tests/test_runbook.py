import tempfile
import os
import shutil
import unittest

from prvsnlib.models import Runbook
from tests.helper import runbooks_dir


class TestRunbook(unittest.TestCase):

    def testValidRunbookFile(self):
        name = 'runbook.py'
        path = os.path.join(runbooks_dir(), name)

        runbook = Runbook(path)

        self.assertEqual(runbook.path, path)
        self.assertEqual(runbook.name, name)
        self.assertTrue(runbook.is_runnable)

    def testValidRunbookWithoutExplicitFileName(self):
        path = os.path.join(runbooks_dir())

        runbook = Runbook(path)

        self.assertEqual(runbook.path, os.path.join(path, 'runbook.py'))
        self.assertEqual(runbook.name, 'runbook.py')
        self.assertTrue(runbook.is_runnable)

    # TODO enable test for runbook URLs
    # def testValidRunbookURL(self):
    #     path = 'http://example.org/runbook.py'
    #
    #     runbook = Runbook(path)
    #
    #     self.assertEqual(runbook.path, path)
    #     self.assertEqual(runbook.name, 'runbook.py')
    #     self.assertTrue(runbook.is_runnable)

    def testInvalidRunbook(self):
        path = os.path.join(runbooks_dir(), 'non-existing runbook')

        runbook = Runbook(path)

        self.assertFalse(runbook.is_runnable)

    def testCreate(self):
        d = tempfile.mkdtemp()
        path = os.path.join(d, 'runbooks', 'runbook.py')

        Runbook.create(path)
        self.assertTrue(os.path.isfile(path))

        shutil.rmtree(d)
