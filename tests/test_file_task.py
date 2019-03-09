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


    @property
    def path3(self):
        return '/tmp/dsfsfsdfsdfsdfsfsfsdffsfsdf'

    @property
    def path4(self):
        return '/tmp/lklklklklklklklklklklklklk'

    @property
    def path5(self):
        return '/tmp/fsdfsd/qweqe'

    def clean_all_files(self):
        for path in [
            self.path1,
            self.path2,
            self.path3,
            self.path4,
            self.path5,
        ]:
            if os.path.exists(path):
                os.unlink(path)

        dir5 = os.path.dirname(self.path5)
        if os.path.exists(dir5):
            os.rmdir(dir5)

    def setUp(self):
        self.clean_all_files()

    def tearDown(self):
        self.clean_all_files()

    def testFile(self):

        Provisioner(
            Runbook(self.runbook),
            ['file'],
        ).run()

        self.assertTrue(os.path.exists(self.path1), 'file at ' + self.path1 + ' should exist')
        self.assertTrue(os.path.exists(self.path2), 'file at ' + self.path2 + ' should exist')
        self.assertTrue(os.path.exists(self.path3), 'file at ' + self.path3 + ' should exist')
        self.assertTrue(os.path.exists(self.path4), 'file at ' + self.path4 + ' should exist')
        self.assertTrue(os.path.exists(self.path5), 'file at ' + self.path5 + ' should exist')

        with open(self.path2, 'r') as f:
            contents = f.read()
        self.assertEqual(contents, 'ddd\nbbb\nddd\nccc\n')

        with open(self.path3, 'r') as f:
            contents = f.read()
        self.assertEqual(contents, 'abc')

        with open(self.path4, 'r') as f:
            contents = f.read()
        self.assertEqual(contents, '')
