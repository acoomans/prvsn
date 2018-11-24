import difflib
import errno
import grp
import logging
import mimetypes
import os
import pwd
import shutil
import sys

if sys.version_info < (3, 0):
    from urllib2 import urlopen
else:
    from urllib.request import urlopen

from .string import replace_all


#--- File types

def is_url(text):
    if '://' in text:
        logging.debug(text + ' is a URL')
        return True
    logging.debug(text + ' is not a URL')
    return False


def is_likely_text_file(path):
    if 'text' in mimetypes.guess_type(path)[0]:
        logging.debug(path + ' is likely text')
        return True
    logging.debug(path + ' is not likely text')
    return False

#--- Directories

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            logging.debug('Directory ' + path + ' already exists.')
        else:
            raise e

#--- Ownership

def chown(path, owner=None, group=None, recursive=False):
    uid = pwd.getpwnam(owner).pw_uid if owner else -1
    gid = grp.getgrnam(group).gr_gid if group else -1

    if recursive:
        for root, dirs, files in os.walk(path):
            for d in dirs:
                os.chown(os.path.join(root, d), uid, gid)
            for f in files:
                os.chown(os.path.join(root, f), uid, gid)
    else:
        os.chown(path, uid, gid)

#--- Backup

def backup_file(filepath):
    if os.path.exists(filepath):
        logging.debug('Making backup of ' + filepath)
        shutil.copyfile(filepath, filepath + '.orig')

#--- File contents

def get_file_bytes_or_text(src, relative=None):
    if is_url(src):
        logging.debug('Fetching ' + src + ' from network')
        response = urlopen(src)
        bytes = response.read()
        encoding = response.headers.get_content_charset()
        if encoding:
            return bytes.decode(encoding)
        return bytes
    else:
        logging.debug('Fetching ' + src + ' from local disk')
        if relative:
            rel_src = os.path.join(relative, src)
            if os.path.exists(rel_src):
                src = rel_src
            else:
                logging.debug('files/' + src + ' does not exist')

        if os.path.exists(src):
            if is_likely_text_file(src):
                with open(src, 'r') as f:
                    text = f.read()
                    return text
            else:
                with open(src, 'rb') as f:
                    bytes = f.read()
                    return bytes
        else:
            logging.debug(src + ' does not exist')
            return None


def write_file_bytes_or_text(filepath, bytes_or_text):
    backup_file(filepath)
    if type(bytes_or_text) is bytearray or type(bytes_or_text) is bytes:
        b = bytes_or_text
        with open(filepath, 'wb') as f:
            logging.debug('Writing bytes to ' + filepath + '.')
            f.write(b)
    elif type(bytes_or_text) is str:
        text = bytes_or_text
        with open(filepath, 'w') as f:
            logging.debug('Writing text to ' + filepath + '.')
            f.write(text)
    else:
        raise Exception('write_file_bytes_or_text: argument nor bytes nor text')


def copy_file(src, dest, relative=None, replacements={}, diff=True):
    backup_file(dest)

    original_data = get_file_bytes_or_text(src, relative)
    if not original_data:
        raise Exception(src + ' file not found')

    if replacements:
        if type(original_data) is str:
            new_data = replace_all(original_data, replacements)
            if diff:
                for line in difflib.unified_diff(
                        original_data.splitlines(),
                        new_data.splitlines(),
                        fromfile=dest + '.orig',
                        tofile=dest):
                    logging.info(line.strip())
        else:
            raise Exception('Cannot replace in binary data')
    else:
        new_data = original_data

    write_file_bytes_or_text(dest, new_data)

#--- File contents manipulation

def add_string_if_not_present_in_file(filepath, string, diff=True):
    backup_file(filepath)

    original_data = get_file_bytes_or_text(filepath)
    if not original_data:
        original_data = ''

    if not type(original_data) is str:
        raise Exception('Cannot add line to binary data')

    if string not in original_data:
        new_data = original_data
        if new_data and new_data[-1] != '\n':
            new_data += '\n'
        new_data += string + '\n'

        if diff:
            for line in difflib.unified_diff(
                    original_data.splitlines(),
                    new_data.splitlines(),
                    fromfile=filepath + '.orig',
                    tofile=filepath):
                logging.info(line.strip())

        write_file_bytes_or_text(filepath, new_data)


def delete_string_from_file(filepath, string, diff=True):
    backup_file(filepath)

    original_data = get_file_bytes_or_text(filepath)
    if not original_data:
        original_data = ''

    if not type(original_data) is str:
        raise Exception('Cannot add line to binary data')

    if string in original_data:
        new_data = original_data.replace(string, '')

        if diff:
            for line in difflib.unified_diff(
                    original_data.splitlines(),
                    new_data.splitlines(),
                    fromfile=filepath + '.orig',
                    tofile=filepath):
                logging.info(line.strip())

        write_file_bytes_or_text(filepath, new_data)
