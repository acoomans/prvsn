import os
import zipfile

from ..task import Task, TaskResult

from prvsnlib.tasks.file import ChownTask

from prvsnlib.utils.file import mkdir_p


class ZipAction:
    EXTRACT = 'extract'


class ZipTask(Task):

    def __init__(self, source, dest, action, **kwargs):
        Task.__init__(self, **kwargs)
        self._source = source
        self._dest = dest
        self._action = action

    def __str__(self):
        return 'Zip file'

    def run(self):
        out, err = [], []
        mkdir_p(os.path.dirname(self._dest))

        source = self._source
        if not os.path.exists(self._source):
            source = os.path.join(self._role.path, 'files', self._source)

        try:
            zf = zipfile.ZipFile(source)
            r = zf.extractall(self._dest)
        except OSError as e:
            return TaskResult(error=str(e))

        return TaskResult(output=['Unzipped'])


def unzip(source, dest, owner=None, group=None, action=ZipAction.EXTRACT):
    ZipTask(source, dest, action)
    if owner or group:
        ChownTask(dest, owner, group, recursive=True)
