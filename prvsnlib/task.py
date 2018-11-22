class TaskResult:

    def __init__(self, command=[], output=[], returncode=None, error=[]):
        self._command = command
        self._output = output
        self._returncode = returncode
        self._error = error

    @property
    def command(self):
        return self._command

    @property
    def output(self):
        return self._output

    @property
    def returncode(self):
        if not self._returncode:
            return len(self._error)
        return self._returncode

    @property
    def error(self):
        return self._error



class Task:

    _queue = None
    _runbook = None
    _role = None

    @classmethod
    def set_queue(cls, queue):
        cls._queue = queue

    @classmethod
    def set_runbook(cls, runbook):
        cls._runbook = runbook

    @classmethod
    def set_role(cls, role):
        cls._role = role

    @property
    def secure(self):
        return self._secure

    def __init__(self, secure=False, user=None):
        self.__class__._queue.append(self)

        self._runbook = self.__class__._runbook
        self._role = self.__class__._role

        self._secure = secure
        self.user = user

    def run(self):
        return TaskResult(
            command=['None'],
            output=['No output'],
            error = ['Task run not implemented']
        )
