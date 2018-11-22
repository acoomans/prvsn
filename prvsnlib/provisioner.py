import getpass
import importlib
import logging
import os
import sys

import prvsnlib.log

from prvsnlib.queue import Queue
from prvsnlib.role import Role
from prvsnlib.task import Task


class Provisioner:

    def __init__(self, runbook, roles, queue=Queue(), extra_imports=None, share_locals=False):
        if extra_imports is None:
            extra_imports = {}
        logging.debug('Provisioner init.')

        self._runbook = runbook
        self._roles = roles

        self._queue = queue
        Task.set_queue(queue)
        Task.set_runbook(self._runbook)

        self._extra_imports = extra_imports
        self._share_locals = share_locals
        self._run_locals = {}

    @staticmethod
    def builtin_imports():
        logging.debug('Provisioner builtin imports.')
        return {
            'prvsnlib.tasks': ['*'],
        }

    def add_task(self, task):
        self._queue.append(task)

    def run_locals(self):
        logging.debug('Provisioner creating run locals.')
        if not self._run_locals or not self._share_locals:
            run_locals = {}
            to_import = self.builtin_imports()
            to_import.update(self._extra_imports)
            for module_name, symbols in to_import.items():
                module = importlib.import_module(module_name)
                for symbol in symbols:
                    if symbol == '*':
                        run_locals.update(module.__dict__)
                    else:
                        run_locals[symbol] = getattr(module, symbol)
            self._run_locals = run_locals
        return self._run_locals

    @staticmethod
    def user_check():
        logging.info('Running Provisioner as user "' + getpass.getuser() + '"')
        if getpass.getuser() != 'root':
            logging.warning('Provisioning is not running as root (add --sudo)')

    def run(self):
        self.user_check()

        logging.header('Runbook ' + self._runbook.path)
        self.build_roles()
        self.run_tasks()

    def build_roles(self):
        logging.debug('Provisioner building roles.')
        for role in self._roles:
            role = Role('role', os.path.join(self._runbook.path, 'roles', role))
            Task.set_role(role)

            with open(role.main_file) as f:
                code = compile(f.read(), role.path, 'exec')
                exec(code, self.run_locals())

    def run_tasks(self):
        logging.debug('Provisioner running tasks.')

        if not self._queue.tasks:
            logging.error('No tasks. Nothing to do.')

        for task in self._queue.tasks:
            logging.header(str(task))

            result = task.run()

            if task.secure:
                logging.info('(secure: output omitted)')
            else:
                if result.command:
                    for line in result.command:
                        logging.info(line)

                if result.output:
                    for line in result.output:
                        logging.info(line)

            exit_code = 0

            if result.error:
                for line in result.error:
                    logging.error(line)
                logging.error('error')
                exit_code = 1

            if result.returncode is None:
                pass
            elif result.returncode == 0:
                logging.debug('return code: ' + str(result.returncode))
            elif result.returncode > 0:
                logging.error('return code: ' + str(result.returncode))
                exit_code = 1

            if exit_code:
                logging.error('Failed.')
                sys.exit(exit_code)

        logging.success('Provisioned.')
