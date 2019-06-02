import logging
import os
import shutil
import tempfile
import unittest

from prvsnlib.utils.file import (
    is_likely_text_file,
    add_string_if_not_present_in_file,
    delete_string_from_file,
    get_file_bytes_or_text,
    copy_file,
)
from prvsnlib.utils.string import is_string
from tests.helper import unittest_dir, unittest_file

verbose = False
if verbose:
    logging.basicConfig(format='%(message)s', level=logging.INFO)


class TestFileTypes(unittest.TestCase):

    def testTextFile(self):
        file = unittest_file('file.txt')
        self.assertTrue(is_likely_text_file(file))

    def testBinaryFile(self):
        file = unittest_file('file.png')
        self.assertFalse(is_likely_text_file(file))


class TestFileCase(unittest.TestCase):

    def setUp(self):
        self.d = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.d)

    def setup_file(self, file):
        src = os.path.join(unittest_dir(), file)
        dst = os.path.join(self.d, file)
        shutil.copyfile(src, dst)
        return dst

    def assertSameFiles(self, file1, file2):
        with open(file1, 'r') as f:
            data1 = f.readlines()
        with open(file2, 'r') as f:
            data2 = f.readlines()
        self.assertEqual(data1, data2)

    def assertFileContains(self, file, pattern, times=1):
        with open(file) as f:
            data = f.readlines()
        if times == '+':
            self.assertGreater(data.count(pattern), 0, 'the file %s should contain at least one "%s"' % (file, pattern))
        elif isinstance(times, int):
            self.assertEqual(data.count(pattern), times, 'the file %s should contain %i "%s"' % (file, times, pattern))


class TestFileAddAndDelete(TestFileCase):

    def testAddFileNotExist(self):
        path = os.path.join(self.d, 'testAddFileNotExist.txt')

        add_string_if_not_present_in_file(path, 'hello')

        self.assertTrue(os.path.isfile(path), 'new file should exist')
        self.assertFileContains(path, 'hello\n', 1)

    def testAddStringNotPresent(self):
        name = 'testAddStringNotPresent.txt'
        path = self.setup_file(name)
        self.assertFileContains(path, 'c\n', 0)

        add_string_if_not_present_in_file(path, 'c')

        self.assertTrue(os.path.isfile(path), 'new file should exist')
        self.assertFileContains(path, 'a\n', 1)
        self.assertFileContains(path, 'b\n', 1)
        self.assertFileContains(path, 'c\n', 1)

        backup = path + '.orig'
        self.assertTrue(os.path.isfile(backup), 'backup file should exist')
        self.assertSameFiles(os.path.join(unittest_dir(), name), backup)

    def testAddStringPresent(self):
        name = 'testAddStringPresent.txt'
        path = self.setup_file(name)
        self.assertFileContains(path, 'a\n', 2)

        add_string_if_not_present_in_file(path, 'a')

        self.assertTrue(os.path.isfile(path), 'new file should exist')
        self.assertFileContains(path, 'a\n', 2)
        self.assertFileContains(path, 'b\n', 1)

        backup = path + '.orig'
        self.assertTrue(os.path.isfile(backup), 'backup file should exist')
        self.assertSameFiles(os.path.join(unittest_dir(), name), backup)

    def testDelFileNotExist(self):
        path = os.path.join(self.d, 'testDelFileNotExist.txt')

        delete_string_from_file(path, 'a')
        self.assertFalse(os.path.isfile(path), 'file should not exist')

    def testDelStringPresent(self):
        name = 'testDelStringPresent.txt'
        path = self.setup_file(name)
        self.assertFileContains(path, 'a\n', 2)

        delete_string_from_file(path, 'a')

        self.assertTrue(os.path.isfile(path), 'new file should exist')
        self.assertFileContains(path, 'a\n', 0)
        self.assertFileContains(path, 'b\n', 1)

        backup = path + '.orig'
        self.assertTrue(os.path.isfile(backup), 'backup file should exist')
        self.assertSameFiles(os.path.join(unittest_dir(), name), backup)

    def testDelStringNotPresent(self):
        name = 'testDelStringNotPresent.txt'
        path = self.setup_file(name)
        self.assertFileContains(path, 'c\n', 0)

        delete_string_from_file(path, 'c')

        self.assertTrue(os.path.isfile(path), 'new file should exist')
        self.assertFileContains(path, 'a\n', 2)
        self.assertFileContains(path, 'b\n', 1)
        self.assertFileContains(path, 'c\n', 0)

        backup = path + '.orig'
        self.assertTrue(os.path.isfile(backup), 'backup file should exist')
        self.assertSameFiles(os.path.join(unittest_dir(), name), backup)


class TestFileContents(TestFileCase):

    @property
    def text_file_url(self):
        return 'https://raw.githubusercontent.com/acoomans/prvsn/master/tests/test_file/file.txt'

    @property
    def zip_file_url(self):
        return 'https://raw.githubusercontent.com/acoomans/prvsn/master/tests/test_file/file.zip'

    def test_get_file_text_from_http_url(self):
        contents = get_file_bytes_or_text(self.text_file_url)
        self.assertTrue(contents)
        self.assertTrue(is_string(contents))

    def test_get_file_bytes_from_http_url(self):
        contents = get_file_bytes_or_text(self.zip_file_url)
        self.assertTrue(contents)
        self.assertTrue(type(contents) is bytes)

    def test_get_file_text_from_local_file(self):
        path = unittest_file('file.txt')
        contents = get_file_bytes_or_text(path)
        self.assertTrue(contents)
        self.assertTrue(is_string(contents))

    def test_get_file_bytes_from_local_file(self):
        path = unittest_file('file.zip')
        contents = get_file_bytes_or_text(path)
        self.assertTrue(contents)
        self.assertTrue(type(contents) is bytes or type(contents) is bytearray)

    def test_copy_file_txt(self):
        path = self.setup_file('test_copy_file_txt.txt')

        new = path + '.new'
        copy_file(path, new, replacements={'b':'e'}, diff=verbose)
        self.assertFileContains(new, 'a\n', 1)
        self.assertFileContains(new, 'b\n', 0)
        self.assertFileContains(new, 'e\n', 1)
        self.assertFileContains(new, 'c\n', 1)

    def test_copy_file_bytes(self):
        path = self.setup_file('test_copy_file_bytes.zip')
        with self.assertRaises(Exception):
            copy_file(path, path, replacements={'c': 'e'})

    def test_copy_file_no_src(self):
        path = os.path.join(self.d, 'test_copy_file_no_src.txt')
        with self.assertRaises(Exception):
            copy_file(path, path, replacements={'c': 'e'})
