import getpass
import subprocess

from prvsnlib.utils.run import run
from ..task import Task


class PackageAction:
    UPDATE = 'update'
    UPGRADE = 'upgrade'
    INSTALL = 'install'
    REMOVE = 'remove'

class PackageTask(Task):

    _packageClass = False

    @classmethod
    def package(cls, *args, **kwargs):
        if not cls._packageClass:
            try:
                if subprocess.check_output(['which', 'brew']):
                    cls._packageClass = HomebrewPackageTask
            except:
                pass
            try:
                if subprocess.check_output(['which', 'apt-get']):
                    cls._packageClass = AptPackageTask
            except:
                pass
            try:
                if subprocess.check_output(['which', 'yum']):
                    cls._packageClass = YumPackageTask
            except:
                pass
        return cls._packageClass(*args, **kwargs)

    def __init__(self, name='', action=PackageAction.INSTALL, **kwargs):
        Task.__init__(self, **kwargs)
        self._name = name.split()
        self._action = action

    def __str__(self):
        if self._action == PackageAction.INSTALL:
            return 'Install package'
        elif self._action == PackageAction.REMOVE:
            return 'Remove package'
        elif self._action == PackageAction.UPDATE:
            return 'Update packages list'
        elif self._action == PackageAction.UPGRADE:
            return 'Upgrade all packages'
        return 'Package action "' + str(self._action) + '" not implemented.'

    def run(self):
        return '', 'Not implemented.'


class HomebrewPackageTask(PackageTask):
    def run(self):
        user_cmd = []
        if self.user and self.user != getpass.getuser():
            user_cmd = ['sudo', '-u', self.user]

        cmd, out, ret, err = '', '', '', ''
        if self._action == PackageAction.UPDATE:
            cmd, out, ret, err = run(user_cmd + ['brew', 'update'])
        elif self._action == PackageAction.UPGRADE:
            cmd, out, ret, err = run(user_cmd + ['brew', 'upgrade'] + self._name)
        elif self._action == PackageAction.INSTALL:
            cmd, out, ret, err = run(user_cmd + ['brew', 'install'] + self._name)
            ret = 0 if ret and 'already installed' in out else ret
        elif self._action == PackageAction.REMOVE:
            cmd, out, ret, err = run(user_cmd + ['brew', 'uninstall'] + self._name)
        if err:
            return cmd, err
        if ret:
            return cmd, out
        return cmd+'\n'+out, ''


class AptPackageTask(PackageTask):
    def run(self):
        cmd, out, ret, err = '', '', '', ''
        if self._action == PackageAction.UPDATE:
            cmd, out, ret, err = run(['apt-get', 'update'])
        elif self._action == PackageAction.UPGRADE:
            cmd, out, ret, err = run(['apt-get', 'upgrade', '-y', '--no-install-recommends'] + self._name)
        elif self._action == PackageAction.INSTALL:
            cmd, out, ret, err = run(['apt-get', 'install', '-y', '--no-install-recommends'] + self._name)
        elif self._action == PackageAction.REMOVE:
            cmd, out, ret, err = run(['apt-get', 'remove', '-y'] + self._name)
        if err:
            return cmd, err
        if ret:
            return cmd, out
        return cmd+'\n'+out, ''


class YumPackageTask(PackageTask):
    def run(self):
        cmd, out, ret, err = '', '', '', ''
        if self._action == PackageAction.UPDATE:
            cmd, out, ret, err = run(['yum', 'update'])
        elif self._action == PackageAction.UPGRADE:
            cmd, out, ret, err = run(['yum', 'upgrade', '-y'] + self._name)
        elif self._action == PackageAction.INSTALL:
            cmd, out, ret, err = run(['yum', 'install', '-y'] + self._name)
        elif self._action == PackageAction.REMOVE:
            cmd, out, ret, err = run(['yum', 'remove', '-y'] + self._name)
        if err:
            return cmd, err
        if ret:
            return cmd, out
        return cmd+'\n'+out, ''


def package(*args, **kwargs):
    PackageTask.package(*args, **kwargs)


def homebrew_package(*args, **kwargs):
    HomebrewPackageTask(*args, **kwargs)


def apt_package(*args, **kwargs):
    AptPackageTask(*args, **kwargs)


def yum_package(*args, **kwargs):
    YumPackageTask(*args, **kwargs)