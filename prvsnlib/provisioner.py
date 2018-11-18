import importlib
import logging
import os
import sys

from prvsnlib.utils.colors import Colors

from prvsnlib.queue import Queue
from prvsnlib.runbook import Runbook
from prvsnlib.role import Role
from prvsnlib.task import Task


class Provisioner:

    def __init__(self, runbook, roles, queue=Queue(), extra_imports={}, share_locals=False):

        self._runbook = runbook
        self._roles = roles

        self._queue = queue
        Task.setQueue(queue)
        Task.setRunBook(self._runbook)

        self._extra_imports = extra_imports
        self._share_locals = share_locals
        self._run_locals = {}

    def builtin_imports(self):
        return {
            'prvsnlib.tasks.command': [
                'command',
                'bash',
                'ruby',
            ],
            'prvsnlib.tasks.file': [
                'file',
            ],
            'prvsnlib.tasks.kernel': [
                'module',
            ],
            'prvsnlib.tasks.package': [
                'package',
                'homebrew_package',
                'apt_package',
                'yum_package',
            ],
        }

    def add_task(self, task):
        self._queue.append(task)

    def run_locals(self):
        if not self._run_locals or not self._share_locals:
            run_locals = {}
            to_import = self.builtin_imports()
            to_import.update(self._extra_imports)
            for module_name, symbols in to_import.items():
                module = importlib.import_module(module_name)
                for symbol in symbols:
                    run_locals[symbol] = getattr(module, symbol)
            self._run_locals = run_locals
        return self._run_locals

    def run(self):
        logging.info(Colors.HEADER + Colors.UNDERLINE + '# Runbook ' + self._runbook.path + Colors.END)
        self.build_roles()
        self.run_tasks()

    def build_roles(self):
        for role in self._roles:
            role = Role('role', os.path.join(self._runbook.path, 'roles', role))
            Task.setRole(role)

            with open(role.main_file) as f:
                code = compile(f.read(), role.path, 'exec')
                exec(code, self.run_locals())

    def run_tasks(self):
        for task in self._queue.tasks():
            logging.info(Colors.HEADER + '## ' + str(task) + Colors.END)

            out, err = task.run()
            if task.secure: logging.info('(secure: output omitted)')
            else: logging.info(out)

            if err:
                if not task.secure: logging.info(Colors.FAIL + err + Colors.END)
                logging.info(Colors.FAIL + 'Task failed.' + Colors.END)
                sys.exit(1)