import inspect
import logging
import os
import shutil
import unittest

from prvsnlib.tasks.unarchive import (
    unarchive,
    unzip,
    untar,
)

logging.basicConfig(format='%(message)s', level=logging.INFO)


class TestUnarchive(unittest.TestCase):

    @property
    def zip(self):
        this_file = inspect.getfile(inspect.currentframe())
        this_dir = os.path.dirname(os.path.abspath(this_file))
        return os.path.join(this_dir, 'files', 'test.zip')

    @property
    def test_zip(self):
        return '/tmp/prvsn/test.zip'

    @property
    def dir_zip(self):
        return '/tmp/prvsn/zip/'

    @property
    def content_zip(self):
        return os.path.join(self.dir_zip, 'test.txt')


    @property
    def tar(self):
        this_file = inspect.getfile(inspect.currentframe())
        this_dir = os.path.dirname(os.path.abspath(this_file))
        return os.path.join(this_dir, 'files', 'test.tar.gz')

    @property
    def test_tar(self):
        return '/tmp/prvsn/test.tar.gz'

    @property
    def dir_tar(self):
        return '/tmp/prvsn/tar'

    @property
    def content_tar(self):
        return os.path.join(self.dir_tar, 'file.txt')


    def setUp(self):
        if not os.path.exists('/tmp/prvsn'):
            os.mkdir('/tmp/prvsn')
        shutil.copyfile(self.zip, self.test_zip)
        shutil.copyfile(self.tar, self.test_tar)

    def tearDown(self):
        for f in [
            self.test_zip,
            self.content_zip,
            self.test_tar,
            self.content_tar
        ]:
            if os.path.exists(f):
                os.remove(f)

        for d in [
            self.dir_zip,
            self.dir_tar,
            '/tmp/prvsn'
        ]:
            if os.path.exists(d):
                os.rmdir(d)

    def test_unarchive(self):
        self.assertTrue(os.path.isfile(self.test_zip), 'zip file missing; test set up incorrectly?')

        unarchive(self.test_zip, self.dir_zip)
        self.assertTrue(os.path.isdir(self.dir_zip))
        self.assertTrue(os.path.isfile(self.content_zip))

    def test_unzip(self):
        self.assertTrue(os.path.isfile(self.test_zip), 'zip file missing; test set up incorrectly?')

        unzip(self.test_zip, self.dir_zip)
        self.assertTrue(os.path.isdir(self.dir_zip))
        self.assertTrue(os.path.isfile(self.content_zip))

    def test_untar(self):
        self.assertTrue(os.path.isfile(self.test_tar), 'tar file missing; test set up incorrectly?')

        untar(self.test_tar, self.dir_tar)
        self.assertTrue(os.path.isdir(self.dir_tar))
        self.assertTrue(os.path.isfile(self.content_tar))