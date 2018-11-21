import getpass
import logging
import sys

from prvsnlib.utils.ssh import Ssh

class Remote:

    def __init__(self,
                 hostname='localhost',
                 username=getpass.getuser(),
                 no_copy_keys=False,
                 package='package.pyz',
                 sudo=True):
        self._hostname = hostname
        self._username = username
        self._no_copy_keys = no_copy_keys
        self._package = package
        self._sudo = sudo

    def run(self):

        ssh = Ssh(remote=self._hostname, user=self._username)

        if not self._no_copy_keys:
            ssh.copy_public_keys()

        dest = 'package.pyz'

        logging.header('Sending package to ' + ssh.remote)
        out, err = ssh.copy_to(self._package, dest)
        if err:
            logging.error('Sending package failed.')
            sys.exit(1)
        logging.success('Sent.')

        logging.header('Remotely executing package on ' + ssh.remote)
        out, err = ssh.command(['python', dest], log_level=logging.INFO, sudo=self._sudo)
        if err:
            logging.error('Remotely executing package failed.')
            sys.exit(1)
        logging.success('Executed.')