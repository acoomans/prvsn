import os
import pwd

from prvsnlib.utils.file import mkdir_p, get_replace_write_file
from ..task import Task, TaskResult


class FileAction:
    ADD = 'add'


class FileTask(Task):

    def __init__(self, source, dest, owner, replacements, action, secure):
        Task.__init__(self, secure)
        self._source = source
        self._dest = dest
        self._owner = owner
        self._action = action
        self._replacements = replacements

    def __str__(self):
        return 'Setting up file "' + self._dest + '"'

    def run(self):
        mkdir_p(os.path.dirname(self._dest))
        out, err = get_replace_write_file(self._source,
                                      os.path.join(self._role.path, 'files'),
                                      self._replacements,
                                      self._dest)

        try:
            uid = pwd.getpwnam(self._owner).pw_uid if self._owner else -1
            gid = pwd.getgrnam(self._group).gr_gid if self._group else -1
            os.chown(self._dest, uid, gid)
        except OSError as e:
            err.append('Could not change file ownership.')

        return TaskResult(output=out, error=err)


def file(source, dest, replacements=None, owner=None, action=FileAction.ADD, secure=False):
    if replacements is None:
        replacements = {}
    FileTask(source, dest, replacements, action, secure)
