import logging
import subprocess

from prvsnlib.utils.run import Run


class FiletypeHandlerType:
    DUTI = 'duti'


class FiletypeHandlerTask:

    _file_handler_tool = None

    @classmethod
    def file_handler_tool(cls, *args, **kwargs):
        if not cls._file_handler_tool:
            try:
                if subprocess.check_output(['which', 'duti']):
                    cls._file_handler_tool = FiletypeHandlerType.DUTI
            except Exception:
                pass
        return cls._file_handler_tool

    def __init__(self, extension, handler):
        self._extension = extension
        self._handler = handler

    def run(self):
        logging.header('File ' + self._extension + ' handled by ' + self._handler)
        file_handler_tool = self.__class__.file_handler_tool()
        if file_handler_tool == FiletypeHandlerType.DUTI:
            return Run(['duti', '-s', self._handler, self._extension, 'all']).run()
        raise Exception('No tool available for handling file types.')


def file_handler(extension, handler):
    FiletypeHandlerTask(extension, handler).run()
