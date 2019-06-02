import os


class Package:

    # TODO handle package URLs

    DEFAULT_FILENAME = 'package.pyz'

    @staticmethod
    def is_valid_filename(path):
        return len(os.path.basename(path)) > 4 and path.endswith('.pyz')

    def __init__(self, path):
        if not self.is_valid_filename(path):
            path = os.path.join(path, Package.DEFAULT_FILENAME)
        self._path = path

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.name)

    def __str__(self):
        return 'package %s' % self.path

    @property
    def path(self):
        return self._path

    @property
    def name(self):
        return os.path.basename(self._path)

    @property
    def is_applicable(self):
        return self.is_valid_filename(self._path) and os.path.isfile(self._path)
