
import os
import unittest
import shlex
import sys

parent_dir = os.path.dirname(__file__)
prvsn_path = os.path.join(parent_dir, '..', 'scripts', 'prvsn')

if sys.version_info < (3, 0):
    import imp
    prvsn = imp.load_source('prvsn', prvsn_path)
else:
    import importlib
    from importlib.machinery import SourceFileLoader
    prvsn = SourceFileLoader("prvsn", prvsn_path).load_module()

from tests.helper import packages_dir, runbooks_dir
from prvsnlib.models import Package, Runbook, LocalTarget, RemoteTarget


class TestArgs(unittest.TestCase):

    def testArgsForRunbooks(self):
        r0 = os.path.join(runbooks_dir(), 'runbook0.py')
        r1 = os.path.join(runbooks_dir(), 'runbook1.py')

        args = prvsn.parser().parse_args(shlex.split('run %s %s' % (r0, r1)))
        runbooks, packages, targets = prvsn.parse_extra(args)

        self.assertEqual(len(runbooks), 2)
        self.assertIsInstance(runbooks[0], Runbook)
        self.assertEqual(runbooks[0].path, r0)
        self.assertIsInstance(runbooks[1], Runbook)
        self.assertEqual(runbooks[1].path, r1)

        self.assertListEqual(packages, [])

        self.assertListEqual(targets, [LocalTarget()])

    def testArgsForPackage(self):
        p0 = os.path.join(packages_dir(), 'package.pyz')

        args = prvsn.parser().parse_args(shlex.split('run %s' % p0))
        runbooks, packages, targets = prvsn.parse_extra(args)

        self.assertListEqual(runbooks, [])

        self.assertEqual(len(packages), 1)
        self.assertIsInstance(packages[0], Package)
        self.assertEqual(packages[0].path, p0)

        self.assertListEqual(targets, [LocalTarget()])

    def testArgsForHostname(self):
        h0 = 'localhost'
        h1 = '127.0.0.1'
        h2 = '192.168.0.1'
        h3 = 'example.org'

        args = prvsn.parser().parse_args(shlex.split('run %s %s %s %s' % (h0, h1, h2, h3)))
        runbooks, packages, targets = prvsn.parse_extra(args)

        self.assertListEqual(runbooks, [])

        self.assertListEqual(packages, [])

        self.assertEqual(len(targets), 4)
        self.assertIsInstance(targets[0], RemoteTarget)
        self.assertEqual(targets[0].name, h0)
        self.assertIsInstance(targets[1], RemoteTarget)
        self.assertEqual(targets[1].name, h1)
        self.assertIsInstance(targets[2], RemoteTarget)
        self.assertEqual(targets[2].name, h2)
        self.assertIsInstance(targets[3], RemoteTarget)
        self.assertEqual(targets[3].name, h3)

    def testAllArgs(self):
        r0 = os.path.join(runbooks_dir(), 'runbook0.py')
        p0 = os.path.join(packages_dir(), 'package.pyz')
        h0 = 'localhost'

        args = prvsn.parser().parse_args(shlex.split('run %s %s %s' % (h0, p0, r0)))
        runbooks, packages, targets = prvsn.parse_extra(args)

        self.assertEqual(len(runbooks), 1)
        self.assertIsInstance(runbooks[0], Runbook)
        self.assertEqual(runbooks[0].path, r0)

        self.assertEqual(len(packages), 1)
        self.assertIsInstance(packages[0], Package)
        self.assertEqual(packages[0].path, p0)

        self.assertEqual(len(targets), 1)
        self.assertIsInstance(targets[0], RemoteTarget)
        self.assertEqual(targets[0].name, h0)
