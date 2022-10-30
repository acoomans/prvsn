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
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(tar, dest)

        if owner or group:
            chown(dest, owner, group, recursive=True)
    else:
        raise Exception('Invalid action')
