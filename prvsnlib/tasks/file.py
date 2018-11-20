import os

from prvsnlib.utils.file import mkdir_p, get_replace_write_file
from ..task import Task


class FileAction:
    ADD = 'add'


class FileTask(Task):

    def __init__(self, source, dest, replacements, action, secure):
        Task.__init__(self, secure)
        self._source = source
        self._dest = dest
        self._action = action
        self._replacements = replacements

    def __str__(self):
        return 'Setting up file "' + self._dest + '"'

    def run(self):
        mkdir_p(os.path.dirname(self._dest))
        return get_replace_write_file(self._source,
                                      os.path.join(self._role.path, 'files'),
                                      self._replacements,
                                      self._dest)


def file(source, dest, replacements=None, action=FileAction.ADD, secure=False):
    if replacements is None:
        replacements = {}
    FileTask(source, dest, replacements, action, secure)
