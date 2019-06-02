import getpass
import unittest

from prvsnlib.remote import Remote

class TestRemote(unittest.TestCase):

    def testRemoteStringEmpty(self):
        remote = ''
        self.assertTrue(Remote(remote).username, getpass.getuser())
        self.assertTrue(Remote(remote).hostname, 'localhost')
        self.assertTrue(Remote(remote).port, 22)

    def testRemoteStringHost(self):
        remote = 'myhost'
        self.assertTrue(Remote(remote).username, getpass.getuser())
        self.assertTrue(Remote(remote).hostname, 'myhost')
        self.assertTrue(Remote(remote).port, 22)

    def testRemoteStringUserHost(self):
        remote = 'myuser@myhost'
        self.assertTrue(Remote(remote).username, 'myuser')
        self.assertTrue(Remote(remote).hostname, 'myhost')
        self.assertTrue(Remote(remote).port, 22)

    def testRemoteStringHostPort(self):
        remote = 'myhost:11'
        self.assertTrue(Remote(remote).username, getpass.getuser())
        self.assertTrue(Remote(remote).hostname, 'myhost')
        self.assertTrue(Remote(remote).port, 11)

    def testRemoteStringUserHostPort(self):
        remote = 'myuser@myhost:11'
        self.assertTrue(Remote(remote).username, 'myuser')
        self.assertTrue(Remote(remote).hostname, 'myhost')
        self.assertTrue(Remote(remote).port, 11)
































