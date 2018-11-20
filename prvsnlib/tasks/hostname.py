from ..task import Task
from prvsnlib.utils.run import run


class HostnameTask(Task):

    def __init__(self, name, secure):
        Task.__init__(self, secure)
        self._name = name

    def __str__(self):
        return 'Hostname ' + self._name

    def run(self):
        cmd, out, ret, err = run(['hostnamectl', 'set-hostname', self._name])
        return cmd + '\n' + out, err


def hostname(name, secure=False):
    HostnameTask(name, secure)
