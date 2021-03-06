import logging
import os
import textwrap

from .role import Role
from .utils.file import mkdir_p


class Runbook:

    def __init__(self, path):
        self._path = path
        self._roles = None

    def __repr__(self):
        return '<Runbook ' + self.name + '>'

    @property
    def path(self):
        return self._path

    @property
    def name(self):
        return os.path.basename(self._path)

    @property
    def roles(self):
        if self._roles is None:
            roles = []
            roles_path = os.path.join(self._path, 'roles')
            if os.path.exists(roles_path):
                for directory in os.listdir(roles_path):
                    directory_path = os.path.join(self._path, 'roles', directory)
                    if os.path.isdir(directory_path):
                        main_path = os.path.join(directory_path, 'main.py')
                        if os.path.isfile(main_path):
                            role = Role(directory_path)
                            roles.append(role)
            self._roles = roles
        return self._roles


def init_runbook(path):
    logging.info('Initializing runbook "' + path + '"')

    roles_path = os.path.join(path, 'roles')
    mkdir_p(roles_path)

    base_roles_path = os.path.join(roles_path, 'base')
    mkdir_p(base_roles_path)

    main_base_roles_path = os.path.join(base_roles_path, 'main.py')
    with open(main_base_roles_path, 'w') as f:
        data = textwrap.dedent('''
            # This is a template for a role

            bash('echo "Hello World!"')

            # package('my_package')
            
            # file(
            #   'example.conf', 
            #   '/etc/example.conf', 
            #   replacements={
            #       'old_string': 'new_string'
            #   }
            # )
        ''').strip()
        f.write(data)

    files_base_roles_path = os.path.join(base_roles_path, 'files')
    mkdir_p(files_base_roles_path)

    with open(os.path.join(files_base_roles_path, 'example.conf'), 'w') as f:
        data = textwrap.dedent('''
            my_variable = old_string
        ''')
        f.write(data)
