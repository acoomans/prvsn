import logging
import os
import textwrap

import prvsnlib.log
from prvsnlib.utils.file import makedirs

class Runbook:

    # TODO handle runbook URLs

    DEFAULT_FILENAME = 'runbook.py'

    @staticmethod
    def is_valid_filename(path):
        return len(os.path.basename(path)) > 3 and path.endswith('.py')

    @classmethod
    def create(cls, path):
        if not cls.is_valid_filename(path):
            path = os.path.join(path, Runbook.DEFAULT_FILENAME)

        logging.header('Creating runbook %s' % path)

        makedirs(os.path.dirname(path))
        with open(path, 'w') as f:
            f.write(textwrap.dedent('''
                    # This is a template for a runbook

                    bash('echo "Hello World!"')

                    # package('my_package')

                    # file(
                    #   src='example.conf', 
                    #   dst='/etc/example.conf', 
                    #   replacements={
                    #       'old_string': 'new_string'
                    #   }
                    # )
                ''').strip())

        logging.success('Runbook created.')
        return Runbook(path)

    def __init__(self, path):
        if not self.is_valid_filename(path):
            path = os.path.join(path, Runbook.DEFAULT_FILENAME)
        self._path = path

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.name)

    def __str__(self):
        return 'runbook %s' % self.path

    @property
    def path(self):
        return self._path

    @property
    def name(self):
        return os.path.basename(self._path)

    @property
    def is_runnable(self):
        return self.is_valid_filename(self._path) and os.path.isfile(self._path)
