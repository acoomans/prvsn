import difflib
import errno
import grp
import logging
import mimetypes
import os
import pwd
import shutil
import subprocess
import sys

if sys.version_info < (3, 0):
    from urllib2 import urlopen
else:
    from urllib.request import urlopen

from .string import replace_all, is_string

BACKUP_EXTENSION = '.orig'


# --- File types

def is_url(text):
    if '://' in text:
        logging.debug('%s is a URL' % text)
        return True
    logging.debug('%s is not a URL' % text)
    return False


def is_likely_text_file(url):
    result = False
    type = mimetypes.guess_type(url)[0]
    logging.debug('Guessing filetype %s for %s' % (str(type), str(url)))
    if type:
        if 'text' in str(type).lower():
            result = True
    else:
        try:
            output = subprocess.check_output(['file', url])
            if 'text' in output.decode("utf-8").lower():
                result = True
        except subprocess.CalledProcessError as e:
            pass

    if result:
        logging.debug('%s is likely text' % url)
    else:
        logging.debug('%s is likely not text' % url)
    return result


# --- Directories

def makedirs(path):
    if path:
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno == errno.EEXIST and os.path.isdir(path):
                logging.debug('Directory %s already exists' % path)
            else:
                raise e


# --- Ownership

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


# --- Backup

def backup_file(filepath):
    if os.path.exists(filepath):
        logging.debug('Making backup of %s' % filepath)
        shutil.copyfile(filepath, filepath + BACKUP_EXTENSION)


# --- File contents

def get_file_bytes_or_text(src, relative=None):
    if is_url(src):
        logging.debug('Fetching %s from network' % src)
        response = urlopen(src)
        b = response.read()

        encoding = None
        if 'get_content_charset' in dir(response.headers): # python 3 only
            encoding = response.headers.get_content_charset()
        elif is_likely_text_file(src):
            encoding = 'utf-8'

        if encoding:
            return b.decode(encoding)
        return b
    else:
        logging.debug('Fetching %s from local disk' % src)
        if relative:
            rel_src = os.path.join(relative, src)
            if os.path.exists(rel_src):
                src = rel_src
            else:
                logging.debug('files/%s does not exist' % src)

        if os.path.exists(src):
            if is_likely_text_file(src):
                with open(src, 'r') as f:
                    text = f.read()
                    return text
            else:
                with open(src, 'rb') as f:
                    b = bytearray(f.read())
                    return b
        else:
            logging.debug('%s does not exist' % src)
            return None


def write_file_bytes_or_text(filepath, bytes_or_text):
    backup_file(filepath)
    if type(bytes_or_text) is bytearray or type(bytes_or_text) is bytes:
        b = bytes_or_text
        with open(filepath, 'wb') as f:
            logging.debug('Writing bytes to %s' % filepath)
            f.write(b)
    elif is_string(bytes_or_text):
        text = bytes_or_text
        with open(filepath, 'w') as f:
            logging.debug('Writing text to %s' % filepath)
            f.write(text)
    else:
        raise Exception('argument nor bytes nor text')


def copy_file(src, dest, relative=None, replacements={}, diff=True):
    backup_file(dest)

    original_data = get_file_bytes_or_text(src, relative)
    if not original_data:
        raise Exception('%s file not found' % src)

    if replacements:
        if is_string(original_data):
            new_data = replace_all(original_data, replacements)
            if diff:
                for line in difflib.unified_diff(
                        original_data.splitlines(),
                        new_data.splitlines(),
                        fromfile=dest + BACKUP_EXTENSION,
                        tofile=dest):
                    logging.info(line.strip())
        else:
            raise Exception('Cannot replace in binary data')
    else:
        new_data = original_data

    write_file_bytes_or_text(dest, new_data)


def add_string_if_not_present_in_file(filepath, string, diff=True):
    backup_file(filepath)

    original_data = get_file_bytes_or_text(filepath)
    if not original_data:
        original_data = ''

    if not is_string(original_data):
        raise Exception('Cannot add line to binary data (%s)' % str(type(original_data)))

    if string not in original_data:
        new_data = original_data
        if new_data and new_data[-1] != '\n':
            new_data += '\n'
        new_data += string + '\n'

        if diff:
            for line in difflib.unified_diff(
                    original_data.splitlines(),
                    new_data.splitlines(),
                    fromfile=filepath + BACKUP_EXTENSION,
                    tofile=filepath):
                logging.info(line.strip())

        write_file_bytes_or_text(filepath, new_data)


def delete_string_from_file(filepath, string, diff=True):
    backup_file(filepath)

    original_data = get_file_bytes_or_text(filepath)
    if not original_data:
        original_data = ''

    if not is_string(original_data):
        raise Exception('Cannot add line to binary data')

    if string in original_data:
        new_data = original_data.replace(string, '')

        if diff:
            for line in difflib.unified_diff(
                    original_data.splitlines(),
                    new_data.splitlines(),
                    fromfile=filepath + BACKUP_EXTENSION,
                    tofile=filepath):
                logging.info(line.strip())

        write_file_bytes_or_text(filepath, new_data)
