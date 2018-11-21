import getpass

from prvsnlib.utils.run import run
from ..task import Task


class CommandAction:
    RUN = 'run'


class CommandTask(Task):

    def __init__(self, interpreter, cmd, action=CommandAction.RUN, **kwargs):
        Task.__init__(self, **kwargs)
        self._interpreter = interpreter
        self._cmd = cmd
        self._action = action

    def __str__(self):
        return 'Run "' + self._interpreter[0] + '" command'

    def run(self):
        user_cmd = []
        if self.user and self.user != getpass.getuser():
            user_cmd = ['sudo', '-u', self.user]

        return run(user_cmd + self._interpreter, stdin=self._cmd)


def command(*args, **kwargs):
    CommandTask(*args, **kwargs)


def bash(*args, **kwargs):
    CommandTask(['bash', '-e'], *args, **kwargs)


def ruby(*args, **kwargs):
    CommandTask(['ruby'], *args, **kwargs)
