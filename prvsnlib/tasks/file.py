import grp
import os
import pwd


from prvsnlib.utils.file import mkdir_p, get_replace_write_file
from ..task import Task, TaskResult


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
        out, err = [], []
        mkdir_p(os.path.dirname(self._dest))
        if self._source:
            out, err = get_replace_write_file(self._source,
                                          os.path.join(self._role.path, 'files'),
                                          self._replacements,
                                          self._dest)
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
        try:
            uid = pwd.getpwnam(self._owner).pw_uid if self._owner else -1
            gid = grp.getgrnam(self._group).gr_gid if self._group else -1

            out, err = [], []
            if self._recusive:
                for root, dirs, files in os.walk(self._path):
                    for d in dirs:
                        os.chown(os.path.join(root, d), uid, gid)
                    for f in files:
                        os.chown(os.path.join(root, f), uid, gid)
            return TaskResult(output='changed.')
        except OSError as e:
            return TaskResult(error=str(e))


def file(source, dest, replacements=None, owner=None, group=None, action=FileAction.ADD, secure=False):
    if replacements is None:
        replacements = {}
    FileTask(source, dest, replacements, action, secure)
    if owner or group:
        ChownTask(dest, owner, group, recursive=False)


def chown(path, owner=None, group=None, recursive=True):
    ChownTask(path, owner, group, recursive)