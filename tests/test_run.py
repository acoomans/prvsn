import logging
import subprocess
import unittest

import prvsnlib.log
from prvsnlib.utils.run import Run


logging.root.setLevel(logging.DEBUG)


class TestRun(unittest.TestCase):

    def assertJoinedEqual(self, gen, v, msg=None):
        l = ''.join([x for x in gen])
        self.assertEqual(l, v, msg)

    def assertInJoinedEqual(self, gen, v, msg=None):
        l = ''.join([x for x  in gen])
        self.assertTrue(v in l, msg)

    def testProcessSimpleOutput(self):
        p = Run(['echo', 'hello']).run()
        self.assertJoinedEqual(p.commands, 'echo hello', 'incorrect command')
        self.assertJoinedEqual(p.output, 'hello', 'incorrect output')

    def testProcessMultilineOutput(self):
        p = Run(['echo', 'hello\nbye']).run()
        self.assertJoinedEqual(p.commands, 'echo hello\nbye', 'incorrect command')
        self.assertJoinedEqual(p.output, 'hellobye', 'incorrect output')

    def testProcessStdin(self):
        p = Run(['cat'], stdin='hello\nwhatsup\nbye').run()
        self.assertJoinedEqual(p.commands, '(cat) hello(cat) whatsup(cat) bye', 'incorrect command')
        self.assertJoinedEqual(p.output, 'hellowhatsupbye', 'incorrect output')

    def testProcessErrorReturn(self):
        with self.assertRaises(subprocess.CalledProcessError):
            p = Run(['test', '-n', '']).run()
            self.assertJoinedEqual(p.commands, 'test -n ', 'incorrect command')
            self.assertJoinedEqual(p.output, '', 'incorrect output')

    def testProcessInvalidCommand(self):
        with self.assertRaises(Exception):
            p = Run(['fjksdhfkljsahfjshaf']).run()
            self.assertJoinedEqual(p.commands, 'fjksdhfkljsahfjshaf', 'incorrect command')
            self.assertInJoinedEqual(p.output, 'No such file or directory', 'incorrect output')
