import inspect
import os
import subprocess
import tempfile
import unittest

from prvsnlib.models import Runbook, Package


# --- Files and directories

def unittest_dir():
    for info in inspect.getouterframes(inspect.currentframe()):
        # locals = info.frame.f_locals
        frame = info[0]
        locals = frame.f_locals
        if 'self' in locals:
            obj = locals['self']
            if isinstance(obj, unittest.TestCase):
                file = os.path.abspath(inspect.getfile(frame))
                name, extension = os.path.splitext(file)
                return name

def unittest_file(name):
    return os.path.join(runbooks_dir(), name)

def runbooks_dir():
    return unittest_dir()


def runbook(name):
    return Runbook(os.path.join(runbooks_dir(), name))


def packages_dir():
    return unittest_dir()


def package(name):
    return Package(os.path.join(packages_dir(), name))


# --- SSH

class enable_self_ssh:

    def __init__(self, path=os.path.join(os.path.expanduser("~"), '.ssh')):
        self._path = path

    @property
    def ssh_dir(self):
        return self._path

    @property
    def priv_key_path(self):
        return self._key_path

    @property
    def pub_key_path(self):
        return self._key_path + '.pub'

    @property
    def authorized_keys_path(self):
        return os.path.join(self.ssh_dir, 'authorized_keys')

    def __enter__(self):

        self._key_path = tempfile.mktemp(dir=self.ssh_dir)

        subprocess.run(['ssh-keygen', '-f', self._key_path])
        os.chmod(self.priv_key_path, 0o400)
        os.chmod(self.pub_key_path, 0o400)

        with open(self.pub_key_path, 'r') as src:
            key = src.read()

        if os.path.isfile(self.authorized_keys_path):
            contains_key = False
            with open(self.authorized_keys_path, 'r+') as dst:
                if key not in dst.read():
                    contains_key = True
        if not os.path.isfile(self.authorized_keys_path) or contains_key:
            with open(self.authorized_keys_path, 'a+') as dst:
                dst.write(key)

        return self

    def __exit__(self, type, value, traceback):

        with open(self.pub_key_path, 'r') as src:
            key = src.read()

        contains_key = False
        with open(self.authorized_keys_path, 'r') as dst:
            if key in dst.read():
                contains_key = True
                contents = dst.read()

        if contains_key:
            with open(self.authorized_keys_path, 'w') as dst:
                dst.write(contents.replace(key, ''))

        os.unlink(self.pub_key_path)
        os.unlink(self.priv_key_path)
