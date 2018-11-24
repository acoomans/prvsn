import inspect
import logging
import os
import shutil
import unittest

from prvsnlib.utils.file import (
    add_string_if_not_present_in_file,
    delete_string_from_file,

    write_file_bytes_or_text,
    get_file_bytes_or_text,
    copy_file,

    is_likely_text_file,
)
from prvsnlib.utils.string import is_string

logging.basicConfig(format='%(message)s', level=logging.INFO)


class TestFile(unittest.TestCase):

    def assertSameFiles(self, file1, file2):
        with open(file1, 'r') as f:
            data1 = f.readlines()
        with open(file2, 'r') as f:
            data2 = f.readlines()
        self.assertEqual(data1, data2)

    @property
    def file(self):
        this_file = inspect.getfile(inspect.currentframe())
        this_dir = os.path.dirname(os.path.abspath(this_file))
        return os.path.join(this_dir, 'files', 'file.txt')

    @property
    def test_file(self):
        return '/tmp/prvsn/test.txt'

    @property
    def orig_file(self):
        return '/tmp/prvsn/test.txt.orig'

    @property
    def zip(self):
        this_file = inspect.getfile(inspect.currentframe())
        this_dir = os.path.dirname(os.path.abspath(this_file))
        return os.path.join(this_dir, 'files', 'test.zip')

    @property
    def test_zip(self):
        return '/tmp/prvsn/test.zip'

    @property
    def orig_zip(self):
        return '/tmp/prvsn/test.zip.orig'

    def setUp(self):
        if not os.path.exists('/tmp/prvsn'):
            os.mkdir('/tmp/prvsn')
        shutil.copyfile(self.file, self.test_file)
        shutil.copyfile(self.zip, self.test_zip)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

        if os.path.exists(self.orig_file):
            os.remove(self.orig_file)

        if os.path.exists(self.test_zip):
            os.remove(self.test_zip)

        if os.path.exists(self.orig_zip):
            os.remove(self.orig_zip)

        if os.path.exists('/tmp/prvsn'):
            os.rmdir('/tmp/prvsn')


class TestFileAddAndDelete(TestFile):

    def testAddFileNotExist(self):
        path = '/tmp/blah'
        if os.path.exists(path):
            os.unlink(path)
        add_string_if_not_present_in_file(path, 'a')

        self.assertTrue(os.path.isfile(path), 'new file should exist')

        with open(path) as f:
            data = f.readlines()
        self.assertEqual(data.count('a\n'), 1)

    def testAddNotPresent(self):

        with open(self.test_file) as f:
            data = f.readlines()
        self.assertEqual(data.count('e\n'), 0, 'the test file should contain 0 "e"; test not set up correctly?')

        add_string_if_not_present_in_file(self.test_file, 'e')

        self.assertTrue(os.path.isfile(self.test_file), 'new file should exist')
        self.assertTrue(os.path.isfile(self.orig_file), 'backup file should exist')
        self.assertSameFiles(self.file, self.orig_file)

        with open(self.test_file) as f:
            data = f.readlines()
        self.assertEqual(data.count('a\n'), 5)
        self.assertEqual(data.count('b\n'), 1)
        self.assertEqual(data.count('c\n'), 1)
        self.assertEqual(data.count('d\n'), 1)
        self.assertEqual(data.count('e\n'), 1)

    def testAddPresent(self):

        with open(self.test_file) as f:
            data = f.readlines()
        self.assertEqual(data.count('a\n'), 5, 'the test file should contain 5 "a"; test not set up correctly?')

        add_string_if_not_present_in_file(self.test_file, 'a')

        self.assertTrue(os.path.isfile(self.test_file), 'new file should exist')
        self.assertTrue(os.path.isfile(self.orig_file), 'backup file should exist')
        self.assertSameFiles(self.file, self.orig_file)

        with open(self.test_file) as f:
            data = f.readlines()
        self.assertEqual(data.count('a\n'), 5)
        self.assertEqual(data.count('b\n'), 1)
        self.assertEqual(data.count('c\n'), 1)
        self.assertEqual(data.count('d\n'), 1)

    def testDelFileNotExist(self):
        path = '/tmp/blah'
        if os.path.exists(path):
            os.unlink(path)

        delete_string_from_file(path, '')
        self.assertTrue(os.path.isfile(self.test_file), 'new file should exist')

    def testDelPresent(self):

        with open(self.test_file) as f:
            data = f.readlines()
        self.assertEqual(data.count('a\n'), 5, 'the test file should contain 5 "a"; test not set up correctly?')

        delete_string_from_file(self.test_file, 'a')

        self.assertTrue(os.path.isfile(self.test_file), 'new file should exist')
        self.assertTrue(os.path.isfile(self.orig_file), 'backup file should exist')
        self.assertSameFiles(self.file, self.orig_file)

        with open(self.test_file) as f:
            data = f.readlines()
        self.assertEqual(data.count('a\n'), 0)
        self.assertEqual(data.count('b\n'), 1)
        self.assertEqual(data.count('c\n'), 1)
        self.assertEqual(data.count('d\n'), 1)

    def testDelNotPresent(self):

        with open(self.test_file) as f:
            data = f.readlines()
        self.assertEqual(data.count('e\n'), 0, 'the test file should contain 0 "e"; test not set up correctly?')

        delete_string_from_file(self.test_file, 'e')

        self.assertTrue(os.path.isfile(self.test_file), 'new file should exist')
        self.assertTrue(os.path.isfile(self.orig_file), 'backup file should exist')
        self.assertSameFiles(self.file, self.orig_file)

        with open(self.test_file) as f:
            data = f.readlines()
        self.assertEqual(data.count('a\n'), 5)
        self.assertEqual(data.count('b\n'), 1)
        self.assertEqual(data.count('c\n'), 1)
        self.assertEqual(data.count('d\n'), 1)
        self.assertEqual(data.count('e\n'), 0)


class TestFileContents(TestFile):

    @property
    def test_file_url(self):
        return 'https://raw.githubusercontent.com/acoomans/prvsn/master/tests/files/file.txt'

    @property
    def zip_file_url(self):
        return 'https://raw.githubusercontent.com/acoomans/prvsn/master/tests/files/test.zip'

    def test_get_file_text_from_http_url(self):
        contents = get_file_bytes_or_text(self.test_file_url)
        self.assertTrue(contents)
        self.assertTrue(is_string(contents))

    def test_get_file_bytes_from_http_url(self):
        contents = get_file_bytes_or_text(self.zip_file_url)
        self.assertTrue(contents)
        self.assertTrue(type(contents) is bytes)

    def test_get_file_text_from_local_file(self):
        contents = get_file_bytes_or_text(self.file)
        self.assertTrue(contents)
        self.assertTrue(is_string(contents))

    def test_get_file_bytes_from_local_file(self):
        contents = get_file_bytes_or_text(self.test_zip)
        self.assertTrue(contents)
        self.assertTrue(type(contents) is bytes or type(contents) is bytearray)

    def test_copy_file_txt(self):
        copy_file(self.test_file, self.test_file, replacements={'c':'e'})
        with open(self.test_file) as f:
            data = f.readlines()
        self.assertEqual(data.count('a\n'), 5)
        self.assertEqual(data.count('b\n'), 1)
        self.assertEqual(data.count('c\n'), 0)
        self.assertEqual(data.count('d\n'), 1)
        self.assertEqual(data.count('e\n'), 1)

    def test_copy_file_bytes(self):
        with self.assertRaises(Exception):
            copy_file(self.test_zip, self.test_zip, replacements={'c': 'e'})

    def test_copy_file_no_src(self):
        with self.assertRaises(Exception):
            copy_file('/tmp/fsfrrrrrrrrrrr', self.test_file, replacements={'c': 'e'})


class TestFileType(TestFile):

    def test_is_likely_binary_file_txt(self):
        self.assertTrue(is_likely_text_file(self.file))

    def test_is_likely_binary_file_zip(self):
        self.assertFalse(is_likely_text_file(self.test_zip))
