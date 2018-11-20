import logging

from subprocess import Popen, PIPE, STDOUT, CalledProcessError


def run(commands, stdin=None):
    try:
        logging.debug('Popen.')
        p = Popen(commands, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        if stdin:
            logging.debug('Communicate input as stdin.')
            cmd = ''
            for line in stdin.splitlines():
                if line:
                    cmd += '(' + ' '.join(commands) + ') ' + line + '\n'
            stdout, stderr = p.communicate(stdin.encode('utf-8'))
        else:
            logging.debug('No input. Just running command.')
            cmd = ' '.join(commands)
            stdout, stderr = p.communicate()

        out = stdout.decode('utf-8')
        ret = p.returncode
        err = None
    except CalledProcessError as e:
        logging.debug('Error happened with popen.')
        cmd = e.cmd
        out = e.output
        ret = e.returncode
        err = str(e)
    return cmd, out, ret, err
