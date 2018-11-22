import grp
import os
import pwd


from prvsnlib.utils.file import mkdir_p, get_replace_write_file
from prvsnlib.utils.file import chown as pchown
from ..task import Task, TaskResult


class FileAction:
    ADD = 'add'


class FileTask(Task):

    def __init__(self, source, dest, replacements, diff, action, secure):
        Task.__init__(self, secure)
        self._source = source
        self._dest = dest
        self._replacements = replacements
        self._diff = diff
        self._action = action

    def __str__(self):
        return 'Setting up file "' + self._dest + '"'

    def run(self):
        out, err = [], []
        mkdir_p(os.path.dirname(self._dest))
        if self._source:
            out, err = get_replace_write_file(
                self._source,
                os.path.join(self._role.path, 'files'),
                self._replacements,
                self._dest,
                diff=self._diff)
        return TaskResult(output=out, error=err)


class ChownTask(Task):

    def __init__(self, path, owner, group, recursive):
        Task.__init__(self)
        self._path = path
        self._owner = owner
        self._group = group
        self._recusive = recursive

    def __str__(self):
        return 'Change ownership of file "' + self._path + '"'

    def run(self):
        out, err = pchown(
            self._path,
            self._owner,
            self._group,
            self._recusive,
        )
        return TaskResult(output=out, error=err)


def file(source, dest, replacements=None, owner=None, group=None, diff=True, action=FileAction.ADD, secure=False):
    if replacements is None:
        replacements = {}
    FileTask(source, dest, replacements, diff, action, secure)
    if owner or group:
        ChownTask(dest, owner, group, recursive=False)


def chown(path, owner=None, group=None, recursive=False):
    ChownTask(path, owner, group, recursive)