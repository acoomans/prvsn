import logging
import unittest

import prvsnlib.log
from prvsnlib.utils.run import Process, Process2


logging.root.setLevel(logging.DEBUG)


class TestRun(unittest.TestCase):

    def assertJoinedEqual(self, gen, v, msg=None):
        l = ''.join([x for x in gen])
        self.assertEqual(l, v, msg)

    def assertInJoinedEqual(self, gen, v, msg=None):
        l = ''.join([x for x  in gen])
        self.assertTrue(v in l, msg)

    def testProcessSimpleOutput(self):
        p = Process(['echo', 'hello']).run()
        self.assertJoinedEqual(p.command, 'echo hello', 'incorrect command')
        self.assertJoinedEqual(p.output, 'hello', 'incorrect output')
        self.assertEqual(p.returncode, 0, 'incorrect return')
        self.assertIsNone(p.error, 'incorrect error')

    def testProcessMultilineOutput(self):
        p = Process(['echo', 'hello\nbye']).run()
        self.assertJoinedEqual(p.command, 'echo hello\nbye', 'incorrect command')
        self.assertJoinedEqual(p.output, 'hellobye', 'incorrect output')
        self.assertEqual(p.returncode, 0, 'incorrect return')
        self.assertIsNone(p.error, 'incorrect error')

    def testProcessStdin(self):
        p = Process(['cat'], stdin='hello\nwhatsup\nbye').run()
        self.assertJoinedEqual(p.command, '(cat) hello(cat) whatsup(cat) bye', 'incorrect command')
        self.assertJoinedEqual(p.output, 'hellowhatsupbye', 'incorrect output')
        self.assertEqual(p.returncode, 0, 'incorrect return')
        self.assertIsNone(p.error, 'incorrect error')

    def testProcessErrorReturn(self):
        p = Process(['test', '-n', '']).run()
        self.assertJoinedEqual(p.command, 'test -n ', 'incorrect command')
        self.assertJoinedEqual(p.output, '', 'incorrect output')
        self.assertEqual(p.returncode, 1, 'incorrect return')
        self.assertIsNone(p.error, 'incorrect error')

    def testProcessInvalidCommand(self):
        p = Process(['fjksdhfkljsahfjshaf']).run()
        self.assertJoinedEqual(p.command, 'fjksdhfkljsahfjshaf', 'incorrect command')
        self.assertInJoinedEqual(p.output, 'No such file or directory', 'incorrect output')
        self.assertEqual(p.returncode, 1, 'incorrect return')
        self.assertIsNotNone(p.error, 'incorrect error')

    def testProcess2SimpleOutput(self):
        p = Process2(['/bin/echo', 'hello']).run()
        self.assertJoinedEqual(p.command, '/bin/echo hello', 'incorrect command')
        self.assertJoinedEqual(p.output, 'hello', 'incorrect output')
        self.assertEqual(p.returncode, 0, 'incorrect return')
        self.assertIsNone(p.error, 'incorrect error')

    def testProcess2MultilineOutput(self):
        p = Process2(['/bin/echo', 'hello\nbye']).run()
        self.assertJoinedEqual(p.command, '/bin/echo hello\nbye', 'incorrect command')
        self.assertJoinedEqual(p.output, 'hellobye', 'incorrect output')
        self.assertEqual(p.returncode, 0, 'incorrect return')
        self.assertIsNone(p.error, 'incorrect error')

    def testProcess2Stdin(self):
        p = Process2(['/bin/cat'], stdin='hello\nwhatsup\nbye').run()
        self.assertJoinedEqual(p.command, '(/bin/cat) hello(/bin/cat) whatsup(/bin/cat) bye', 'incorrect command')
        self.assertJoinedEqual(p.output, 'hellowhatsupbye', 'incorrect output')
        self.assertEqual(p.returncode, 0, 'incorrect return')
        self.assertIsNone(p.error, 'incorrect error')

    def testProcess2ErrorReturn(self):
        p = Process2(['/bin/test', '-n', '']).run()
        self.assertJoinedEqual(p.command, '/bin/test -n ', 'incorrect command')
        self.assertJoinedEqual(p.output, '', 'incorrect output')
        self.assertNotEqual(p.returncode, 0, 'incorrect return')
        self.assertIsNone(p.error, 'incorrect error')

    # TODO: fix test; it hangs
    # def testProcess2InvalidCommand(self):
    #     p = Process2(['fjksdhfkljsahfjshaf'])
    #     p.run()
    #     self.assertJoinedEqual(p.command, 'fjksdhfkljsahfjshaf', 'incorrect command')
    #     self.assertInJoinedEqual(p.output, 'No such file or directory', 'incorrect output')
    #     self.assertNotEqual(p.returncode, 0, 'incorrect return')
    #     self.assertIsNotNone(p.error, 'incorrect error')