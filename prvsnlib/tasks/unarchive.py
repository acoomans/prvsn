import logging
import os
import tarfile
import zipfile

from prvsnlib.context import context
from prvsnlib.utils.file import mkdir_p, chown


class UnarchiveAction:
    EXTRACT = 'extract'


def unarchive(*args, **kwargs):
    if args[0].endswith('.zip'):
        unzip(*args, **kwargs)
    elif args[0].endswith('.tar.gz'):
        untar(*args, **kwargs)
    else:
        raise Exception('File extension not handled.')


def unzip(src, dest, owner=None, group=None, action=UnarchiveAction.EXTRACT):
    if action == UnarchiveAction.EXTRACT:
        logging.header('Extract zip file '+ src)

        mkdir_p(os.path.dirname(dest))

        global context

        if not os.path.exists(src):
            src = os.path.join(context.role.path, 'files', src)

        zf = zipfile.ZipFile(src)
        r = zf.extractall(dest)

        if owner or group:
            chown(dest, owner, group, recursive=True)
    else:
        raise Exception('Invalid action')


def untar(src, dest, owner=None, group=None, action=UnarchiveAction.EXTRACT):
    if action == UnarchiveAction.EXTRACT:
        logging.header('Extract tar file '+ src)

        mkdir_p(os.path.dirname(dest))

        global context

        if not os.path.exists(src):
            src = os.path.join(context.role.path, 'files', src)

        with tarfile.open(src) as tar:
            tar.extractall(dest)

        if owner or group:
            chown(dest, owner, group, recursive=True)
    else:
        raise Exception('Invalid action')
