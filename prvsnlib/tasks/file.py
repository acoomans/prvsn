import logging
import os
import sys

if sys.version_info < (3, 0):
    from urlparse import urlparse
else:
    from urllib.parse import urlparse

from prvsnlib.context import context
from prvsnlib.utils.file import mkdir_p, copy_file
from prvsnlib.utils.file import chown as chown_util


class FileAction:
    ADD = 'add'
    REMOVE = 'remove'


def file(src=None, dst=None,
         replacements={},
         owner=None, group=None,
         diff=True,
         action=FileAction.ADD,
         secure=False):

    global context

    if action == FileAction.ADD:
        logging.header('Setting up file ' + dst)

        if not dst:
            if not src:
                raise Exception('No src nor dst specified for file()')
            dst = os.path.basename(urlparse(src).path)
            logging.debug('No destination file specified; assuming ' + dst)

        if not src:
            filename = os.path.basename(urlparse(dst).path)
            if filename:
                path = os.path.join(context.role.path, 'files', filename)
                if os.path.exists(path) and os.path.isfile(path):
                    src = path
                    logging.debug('No source file specified; assuming ' + src)

        base = os.path.basename(dst)
        if base != dst:
            mkdir_p(base)

        if src:
            logging.info('Copying ' + src + ' to ' + dst)

            copy_file(
                src,
                dst,
                replacements=replacements,
                relative=os.path.join(context.role.path, 'files'),
                diff=diff
            )
        else:
            logging.info('Creating empty file ' + dst)

            def touch(path, times=None):
                with open(path, 'a'):
                    os.utime(path, times)

            touch(dst)

        if owner or group:
            chown_util(dst, owner, group, recursive=False)

    elif action == FileAction.REMOVE:
        logging.header('Removing file ' + src)
        os.unlink(src)

    else:
        raise Exception('Invalid action')


def chown(path,
          owner=None, group=None,
          recursive=False):
    logging.header('Changing ownership of file ' + path)
    chown_util(path, owner, group, recursive)