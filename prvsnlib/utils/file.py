import difflib
import errno
import os
import shutil

from urllib.request import urlopen

from .string import replace_all


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def write_file_content(filepath, contents):
    if os.path.exists(filepath):
        shutil.copyfile(filepath, filepath + '.orig')
    with open(filepath, 'w') as f:
        f.write(contents)

def is_url(source):
    return source.startswith('http://') or \
           source.startswith('https://') or \
           source.startswith('file://')

def get_file_contents(source, relative=None):
    contents = None
    if is_url(source):
        response = urlopen(source)
        contents = response.read().decode('utf-8')
    else:
        if relative:
            source = os.path.join(relative, source)
        with open(source, 'r') as f:
            contents = f.read()
    return contents

def get_replace_write_file(source, relative, replacements, filepath):
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                original_data = f.readlines()
            shutil.copyfile(filepath, filepath + '.orig')
        else:
            original_data = []

        if not replacements: replacements = {}

        data = get_file_contents(source, relative)
        new_data = replace_all(data, replacements)
        write_file_content(filepath, new_data)

        out = ''
        for line in difflib.unified_diff(
                original_data,
                new_data.splitlines(keepends=True),
                fromfile=filepath + '.orig',
                tofile=filepath):
            out += line
        return out, ''

    except Exception as e:
        return '', str(e)

def add_string_if_not_present_in_file(filepath, s):
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                original_data = f.readlines()
            shutil.copyfile(filepath, filepath+'.orig')
        else:
            original_data = []

        new_data = original_data.copy()

        need_to_add = True

        for idx in range(len(new_data)):
            line = new_data[idx]
            if s in line:
                need_to_add = False
                break

        if need_to_add:
            new_data.append('\n' + s + '\n')
            with open(filepath, 'w') as file:
                file.writelines(new_data)

        out = ''
        for line in difflib.unified_diff(original_data, new_data, fromfile=filepath+'.orig', tofile=filepath):
            out += line
        return out, ''

    except Exception as e:
        return '', str(e)

def delete_string_from_file(filepath, s):
    try:
        with open(filepath, 'r') as f:
            original_data = f.readlines()

        shutil.copyfile(filepath, filepath+'.orig')
        new_data = original_data.copy()

        need_to_save = False

        idx = 0
        last = len(new_data) - 1
        while idx < last:
            line = new_data[idx]
            if s in line:
                del new_data[idx]
                need_to_save = True
                last -= 1
            else:
                idx += 1

        if need_to_save:
            with open(filepath, 'w') as file:
                file.writelines(new_data)

        out = ''
        for line in difflib.unified_diff(original_data, new_data, fromfile=filepath+'.orig', tofile=filepath):
            out += line
        return out, ''

    except Exception as e:
        return '', [str(e)]