import os
import subprocess
import tempfile
import unittest

from tests.helper import enable_self_ssh


class TestRunbook(unittest.TestCase):

    def testEnableSelfSSHFiles(self):
        tmp = tempfile.mkdtemp()
        with enable_self_ssh(path=tmp) as e:
            self.assertTrue(os.path.isdir(e.ssh_dir))
            self.assertTrue(os.path.isfile(e.priv_key_path))
            self.assertTrue(os.path.isfile(e.pub_key_path))
            self.assertTrue(os.path.isfile(e.authorized_keys_path))
            with open(e.pub_key_path) as pub:
                pub_key = pub.read()
                with open(e.authorized_keys_path) as auth:
                    auth_keys = auth.read()
            self.assertTrue(pub_key in auth_keys)

        with open(e.authorized_keys_path) as auth:
            auth_keys = auth.read()
        self.assertFalse(pub_key in auth_keys)

        self.assertFalse(os.path.isfile(e.priv_key_path))
        self.assertFalse(os.path.isfile(e.pub_key_path))
        os.unlink(e.authorized_keys_path)
        os.rmdir(tmp)

    def testEnableSelfSSHCommand(self):
        with enable_self_ssh() as e:
            output = subprocess.check_output([
                'ssh',
                '-i', e.priv_key_path,
                'localhost',
                'echo "hello"'
            ])
            self.assertTrue('hello' in str(output))
