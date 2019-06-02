import os
import unittest

from prvsnlib.models import Package
from tests.helper import packages_dir


class TestPackage(unittest.TestCase):

    def testValidPackageFile(self):
        name = 'package.pyz'
        path = os.path.join(packages_dir(), name)

        package = Package(path)

        self.assertEqual(package.path, path)
        self.assertEqual(package.name, name)
        self.assertTrue(package.is_applicable)

    def testValidPackageWithoutExplicitFileName(self):
        path = os.path.join(packages_dir())

        package = Package(path)

        self.assertEqual(package.path, os.path.join(path, 'package.pyz'))
        self.assertEqual(package.name, 'package.pyz')
        self.assertTrue(package.is_applicable)

    # TODO enable test for package URLs
    # def testValidPackageURL(self):
    #
    #     path = 'http://example.org/package.pyz'
    #
    #     package = Package(path)
    #
    #     self.assertEqual(package.path, path)
    #     self.assertEqual(package.name, 'package.pyz')
    #     self.assertTrue(package.is_applicable)

    def testInvalidPackage(self):
        path = os.path.join(packages_dir(), 'non-existing package')

        package = Package(path)

        self.assertFalse(package.is_applicable)
