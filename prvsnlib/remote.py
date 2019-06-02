import getpass
import logging
import sys

from prvsnlib.utils.ssh import SSH


class Remote:

    def __init__(self, remote, copy_keys=True, package=None, sudo=False):
        self._remote = remote
        self.copy_keys = copy_keys
        self.package = package
        self.sudo = sudo

    def __repr__(self):
        return '<%s %s@%s:%i>' % (
            self.__class__.__name__,
            self.username,
            self.hostname,
            self.port,
        )

    def __str__(self):
        return '%s@%s:%i' % (
            self.username,
            self.hostname,
            self.port,
        )

    @property
    def username(self):
        return self._remote.split('@')[0] or getpass.getuser()

    @property
    def hostname(self):
        return self._remote.split('@')[-1].split(':')[0] or 'localhost'

    @property
    def port(self):
        return self._remote.split('@')[-1].split(':')[-1] or 22

    def copy_keys_if_needed(self, ssh):
        if not self.copy_keys:
            logging.debug('No-copy-keys specified; skipping copying ssh keys')
            return

        logging.header('Copying ssh keys to %s' % self)
        ssh.copy_keys()

        all_lines = []
        for line in ssh.output:
            logging.debug(line)
            all_lines.append(line)

        if 'skipped because they already exist' in ''.join(all_lines):
            logging.success('Keys already present. Skipped.')
        else:
            if ssh.returncode is None:
                pass
            elif ssh.returncode == 0:
                logging.debug('return code: 0')
                logging.success('Keys copied.')
            elif ssh.returncode > 0:
                logging.debug('return code: ' + str(ssh.returncode))
                logging.error('Failed copying keys.')

    def copy_package_if_needed(self, ssh):
        if not self.package:
            logging.debug('No package specified; skipping copying package')
            return

        logging.header('Copying package to %s' % self)
        ssh.copy_file(self.package)

        for line in ssh.output:
            logging.debug(line)

        exit_code = 0

        if ssh.error:
            for line in ssh.error:
                logging.error(line)
                exit_code = 1

        if ssh.returncode is None:
            pass
        elif ssh.returncode == 0:
            logging.debug('return code: 0')
        elif ssh.returncode > 0:
            logging.error('return code: ' + str(ssh.returncode))
            exit_code = 1

        if exit_code:
            logging.error('Copy package failed.')
            sys.exit(exit_code)

        logging.success('Sent.')

    def execute_package_if_needed(self, ssh):


        logging.header('Remotely executing package on ' + ssh.hostname)


        ssh.run_command(['python', self.package], sudo=self.sudo)

        if ssh.output:
            for line in ssh.output:
                logging.info(line)

        exit_code = 0

        if ssh.error:
            for line in ssh.error:
                logging.error(line)
                exit_code = 1

        if ssh.returncode is None:
            pass
        elif ssh.returncode == 0:
            logging.debug('return code: 0')
        elif ssh.returncode > 0:
            logging.error('return code: ' + str(ssh.returncode))
            exit_code = 1

        if exit_code:
            logging.error('Remotely executing package failed.')
            sys.exit(exit_code)

        logging.success('Remote package executed.')

    def run(self):

        ssh = SSH(
            hostname=self.hostname,
            username=self.username,
            port=self.port
        )

        self.copy_keys_if_needed(ssh)
        self.copy_package_if_needed(ssh)
        self.execute_package(ssh)

        logging.success('Remote provisioned.')
