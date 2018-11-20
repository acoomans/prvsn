import subprocess

from ..task import Task
from prvsnlib.utils.run import run


class FiletypeHandlerType:
    DUTI = 'duti'


class FiletypeHandlerTask(Task):
    _file_handler_tool = None

    def __init__(self, extension='.txt', handler=None, **kwargs):
        Task.__init__(self, **kwargs)
        self._extension = extension
        self._handler = handler

    def __str__(self):
        return 'File "' + self._extension + '" handler: ' + self._handler

    @property
    def file_handler_tool(self):
        if not self.__class__._file_handler_tool:
            try:
                if subprocess.check_output(['which', 'duti']):
                    self.__class__._file_handler_tool = FiletypeHandlerType.DUTI
            except Exception:
                pass
        return self.__class__._file_handler_tool

    def run(self):
        cmd, out, ret, err = '', '', '', ''
        if self.file_handler_tool == FiletypeHandlerType.DUTI:
            cmd, out, ret, err = run(['duti', '-s', self._handler, self._extension, 'all'])
        return cmd + '\n' + out, err


def file_handler(*args, **kwargs):
    FiletypeHandlerTask(*args, **kwargs)
