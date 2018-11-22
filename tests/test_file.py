import inspect
import logging
import os
import shutil
import unittest

from prvsnlib.utils.file import (
    add_string_if_not_present_in_file,
    delete_string_from_file,
    get_file_contents,
    is_likely_text_file
)

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

    def setUp(self):
        if not os.path.exists('/tmp/prvsn'):
            os.mkdir('/tmp/prvsn')
        shutil.copyfile(self.file, self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists(self.orig_file):
            os.remove(self.orig_file)
        if os.path.exists('/tmp/prvsn'):
            os.rmdir('/tmp/prvsn')

    def testAddFileNotExist(self):
        path = '/tmp/blah'
        if os.path.exists(path):
            os.unlink(path)
        out, err = add_string_if_not_present_in_file(path, 'a')
        self.assertTrue(out)
        self.assertFalse(len(err) > 0)
        self.assertTrue(os.path.isfile(self.test_file), 'new file should exist')

    def testAddNotPresent(self):

        with open(self.test_file) as f:
            data = f.readlines()
        self.assertEqual(data.count('e\n'), 0, 'the test file should contain 0 "e"; test not set up correctly?')

        out, err = add_string_if_not_present_in_file(self.test_file, 'e')
        self.assertTrue(out)
        self.assertFalse(err)
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

        out, err = add_string_if_not_present_in_file(self.test_file, 'a')
        self.assertFalse(out)
        self.assertFalse(err)
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
        out, err = delete_string_from_file(path, '')
        self.assertFalse(out)
        self.assertTrue(err)
        self.assertTrue(os.path.isfile(self.test_file), 'new file should exist')

    def testDelPresent(self):

        with open(self.test_file) as f:
            data = f.readlines()
        self.assertEqual(data.count('a\n'), 5, 'the test file should contain 5 "a"; test not set up correctly?')

        out, err = delete_string_from_file(self.test_file, 'a')
        self.assertTrue(out)
        self.assertFalse(err)
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

        out, err = delete_string_from_file(self.test_file, 'e')
        self.assertFalse(out)
        self.assertFalse(err)
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

    def test_get_file_contents_from_http_url(self):
        contents = get_file_contents('http://acoomans.com')
        self.assertTrue(contents)

    def test_get_file_contents_from_file_url(self):
        contents = get_file_contents('file://' + self.file)
        self.assertTrue(contents)

    def test_get_file_contents_from_local_file(self):
        contents = get_file_contents(self.file)
        self.assertTrue(contents)

    @property
    def zip_file(self):
        this_file = inspect.getfile(inspect.currentframe())
        this_dir = os.path.dirname(os.path.abspath(this_file))
        return os.path.join(this_dir, 'files', 'test.zip')

    def test_is_likely_binary_file_txt(self):
        self.assertTrue(is_likely_text_file(self.file))

    def test_is_likely_binary_file_zip(self):
        self.assertFalse(is_likely_text_file(self.zip_file))




