import os

class Runbook:

    def __init__(self, name, path):
        self._name = name
        self._path = path

    @property
    def path(self):
        return self._path

    @property
    def name(self):
        return self._name

    @property
    def metadata_file(self):
        return os.path.join(self._path, 'metadata.py')