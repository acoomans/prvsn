import logging

from subprocess import Popen, PIPE, STDOUT, CalledProcessError


def run(commands, stdin=None):

    class Running():
        def __init__(self, p):
            self._p = p

        @property
        def out(self):
            for line in iter(self._p.stdout.readline, b''):
                output = line.decode('utf-8')
                print(output)
                yield output


    try:
        logging.debug('Popen.')
        p = Popen(commands, stdin=PIPE, stdout=PIPE, stderr=STDOUT, bufsize=0)
        if stdin:
            logging.debug('Communicate input as stdin.')
            cmd = ''
            for line in stdin.splitlines():
                if line:
                    cmd += '(' + ' '.join(commands) + ') ' + line + '\n'
            p.stdin.write(stdin.encode('utf-8'))

            return '', Running(p)

            # for line in iter(p.stdout.readline, b''):
            #     output = line.decode('utf-8')
            #     print(output)
            #     yield output

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
