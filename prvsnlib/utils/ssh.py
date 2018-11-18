import getpass
import logging
import pty
import os


class Ssh:
    def __init__(self, remote='localhost', user=getpass.getuser(), password=None):
        self._remote = remote
        self._user = user
        self._password = password

    def __str__(self):
        return '<SSH ' + self._user + '@' + self._remote + '>'


    def command(self, commands):

        commands = [
            '/usr/bin/ssh',
            self._user + '@' + self._remote,
        ] + commands
        logging.debug('Running "' + ' '.join(commands) + '"')

        pid, child_fd = pty.fork()

        def is_child_pid(pid):
            return not pid

        if is_child_pid(pid):
            os.execv(commands[0], commands)

        password = ''
        password_attempted = False

        output = []
        while True:

            try:
                r = os.read(child_fd, 1024).strip()
                wpid, wret, wres = os.wait4(pid, os.WNOHANG)
            except Exception as e:
                break
            lower = r.lower()

            if b'are you sure you want to continue connecting' in lower:
                logging.debug('Adding host to known hosts')
                os.write(child_fd, b'yes\n')

            elif b'password:' in lower:
                if self._password:
                    password = self._password
                else:
                    password = getpass.getpass()
                    password_attempted = True

                logging.debug('Sending SSH password')
                os.write(child_fd, password.encode('utf-8') + b'\n')

            elif r:
                if password_attempted and password and b'uthentication fail' not in lower:
                    logging.debug('SSH authenticated')
                    self._password = password

                output.append(r.decode('utf-8'))

            if wret:
                err = '\n'.join(output)
                logging.error(err)
                return '', err

        out = ''.join(output)
        logging.debug('SSH command output:\n' + out)
        return out, ''