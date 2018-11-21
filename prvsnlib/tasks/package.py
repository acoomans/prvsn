import getpass
import subprocess

from prvsnlib.utils.run import run
from ..task import Task, TaskResult


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
            except Exception:
                pass
            try:
                if subprocess.check_output(['which', 'apt-get']):
                    cls._packageClass = AptPackageTask
            except Exception:
                pass
            try:
                if subprocess.check_output(['which', 'yum']):
                    cls._packageClass = YumPackageTask
            except Exception:
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
        return TaskResult(error='Not implemented.')


class HomebrewPackageTask(PackageTask):

    def run(self):
        user_cmd = []
        if self.user and self.user != getpass.getuser():
            user_cmd = ['sudo', '-u', self.user]

        if self._action == PackageAction.UPDATE:
            return run(user_cmd + ['brew', 'update'])
        elif self._action == PackageAction.UPGRADE:
            return run(user_cmd + ['brew', 'upgrade'] + self._name)
        elif self._action == PackageAction.INSTALL:
            return run(user_cmd + ['brew', 'install'] + self._name)
        elif self._action == PackageAction.REMOVE:
            return run(user_cmd + ['brew', 'uninstall'] + self._name)
        return TaskResult(error='Action not available')


class CaskPackageTask(PackageTask):

    def run(self):
        user_cmd = []
        if self.user and self.user != getpass.getuser():
            user_cmd = ['sudo', '-u', self.user]

        if self._action == PackageAction.UPDATE:
            return TaskResult(output='No update function for Cask. Ignoring.')
        elif self._action == PackageAction.UPGRADE:
            return run(user_cmd + ['brew', 'cask', 'upgrade'] + self._name)
        elif self._action == PackageAction.INSTALL:
           return run(user_cmd + ['brew', 'cask', 'install'] + self._name)
        elif self._action == PackageAction.REMOVE:
            return run(user_cmd + ['brew', 'cask', 'uninstall'] + self._name)
        return TaskResult(error='Action not available')


class MasPackageTask(PackageTask):

    def run(self):
        user_cmd = []
        if self.user and self.user != getpass.getuser():
            user_cmd = ['sudo', '-u', self.user]

        if self._action == PackageAction.UPDATE:
            return TaskResult(output='No update function for app store. Ignoring.')
        elif self._action == PackageAction.UPGRADE:
            return run(user_cmd + ['mas', 'upgrade'] + self._name)
        elif self._action == PackageAction.INSTALL:
            return run(user_cmd + ['mas', 'install'] + self._name)
        elif self._action == PackageAction.REMOVE:
            return TaskResult(returncode=1, error='No remove function for app store.')
        return TaskResult(error='Action not available')


class AptPackageTask(PackageTask):
    def run(self):
        if self._action == PackageAction.UPDATE:
            return run(['apt-get', 'update'])
        elif self._action == PackageAction.UPGRADE:
            return run(['apt-get', 'upgrade', '-y', '--no-install-recommends'] + self._name)
        elif self._action == PackageAction.INSTALL:
            return run(['apt-get', 'install', '-y', '--no-install-recommends'] + self._name)
        elif self._action == PackageAction.REMOVE:
            return run(['apt-get', 'remove', '-y'] + self._name)
        return TaskResult(error='Action not available')


class YumPackageTask(PackageTask):
    def run(self):
        if self._action == PackageAction.UPDATE:
            return run(['yum', 'update'])
        elif self._action == PackageAction.UPGRADE:
            return run(['yum', 'upgrade', '-y'] + self._name)
        elif self._action == PackageAction.INSTALL:
            return run(['yum', 'install', '-y'] + self._name)
        elif self._action == PackageAction.REMOVE:
            return run(['yum', 'remove', '-y'] + self._name)
        return TaskResult(error='Action not available')


def package(*args, **kwargs):
    PackageTask.package(*args, **kwargs)


def mac_app_store(*args, **kwargs):
    MasPackageTask(*args, **kwargs)


def homebrew_package(*args, **kwargs):
    HomebrewPackageTask(*args, **kwargs)


def cask_package(*args, **kwargs):
    CaskPackageTask(*args, **kwargs)


def apt_package(*args, **kwargs):
    AptPackageTask(*args, **kwargs)


def yum_package(*args, **kwargs):
    YumPackageTask(*args, **kwargs)
