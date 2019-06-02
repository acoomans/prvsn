import logging
import os
import shutil
import tempfile
import textwrap

import prvsnlib
from prvsnlib.utils.file import makedirs
from prvsnlib.utils.zip import zipdir


class Packager:

    def __init__(self, runbooks, tmpdir=None, dest=None, cleanup=True, verbose=False):
        self.runbooks = runbooks
        self.tmpdir = tmpdir
        self.dest = dest
        self.verbose = verbose
        self.cleanup = cleanup

    @property
    def prvsnlib_path(self):
        path = os.path.dirname(prvsnlib.__file__)
        logging.debug('Path to prvsnlib is ' + path)
        return path

    @property
    def package_main_contents(self):
        directory, _ = os.path.split(os.path.dirname(__file__))
        file = os.path.join(directory, 'bootstrap.py')
        contents = open(file).read().replace(
            '#ARGUMENTS#',
            '''
            runbooks = [],
            loglevel = logging.
            ''' % {
                'loglevel': ('DEBUG' if self.verbose else 'INFO')
            }
        )
        return contents

    def build_package(self):
        logging.header('Packaging runbook "%s"' % self.runbook.path)

        if not self._dest:
            fd, self._dest = tempfile.mkstemp(suffix='.pyz')

        dest_path = os.path.dirname(self._dest)
        makedirs(dest_path)

        self.prepare_package()

        logging.debug('Building package at "' + self._dest + '"')

        zipdir(
            self._tmpdir,
            self._dest,
        )

        self.cleanup_package()

        logging.success('Packaged.')
        return self._dest

    def write_package_main(self, path):
        file = os.path.join(path, '__main__.py')
        logging.debug('Writing package main file at "' + file + '"')

        with open(file, 'w') as f:
            f.write(self.package_main_contents)
        os.chmod(file, 0o550)

    def prepare_package(self):
        if not self._tmpdir:
            self._tmpdir = tempfile.mkdtemp()

        if not os.path.exists(self._tmpdir):
            mkdir_p(self._tmpdir)

        logging.debug('Preparing package at "' + self._tmpdir + '"')

        shutil.copytree(
            self.prvsnlib_path,
            os.path.join(self._tmpdir, 'prvsnlib'),
            ignore=shutil.ignore_patterns('*.pyc', '__pycache__')
        )
        shutil.copytree(
            self._runbook.path,
            os.path.join(self._tmpdir, 'runbook')
        )
        self.write_package_main(self._tmpdir)

    def cleanup_package(self):
        if self._cleanup:
            logging.debug('Cleaning up package temp dir')
            shutil.rmtree(self._tmpdir)
