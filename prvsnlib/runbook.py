import os

from .role import Role


class Runbook:

    def __init__(self, name, path):
        self._name = name
        self._path = path
        self._roles = []

    def __repr__(self):
        return '<Runbook "' + self._name + '" (' + self._path + ')>'

    @property
    def path(self):
        return self._path

    @property
    def name(self):
        return self._name

    @property
    def metadata_file(self):
        return os.path.join(self._path, 'metadata.py')

    @property
    def roles(self):
        if not self._roles:
            roles = []
            roles_path = os.path.join(self._path, 'roles')
            if os.path.exists(roles_path):
                for file in os.listdir():
                    file_path = os.path.join(self._path, 'roles', file)
                    if os.path.isdir(file_path):
                        main_path = os.path.join(file_path, 'main.py')
                        if os.path.isfile(main_path):
                            roles.append(Role('role', file_path))
            self._roles = roles

        return self._roles