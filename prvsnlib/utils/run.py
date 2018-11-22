import logging
import os
import subprocess
import sys

STDIN_FILENO = 0
STDOUT_FILENO = 1
STDERR_FILENO = 2

CHILD = 0


class Process():

    def __init__(self, commands, stdin=None):
        self._commands = commands
        self._stdin_data = stdin
        self._returncode = None
        self._exception = None
        self._process = None

    def run(self):
        logging.debug(self.__class__.__name__)

        try:

            logging.debug('Popen.')
            self._process = subprocess.Popen(
                self._commands,
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                bufsize=0, universal_newlines=True)

            if self._stdin_data:
                logging.debug('Writing to stdin.')
                self._process.stdin.write(self._stdin_data)
                self._process.stdin.close()

        except Exception as e:
                self._exception = e
        return self

    @property
    def command(self):
        logging.debug('Process command.')
        if self._stdin_data:
            for line in self._stdin_data.splitlines():
                if line:
                    yield '(' + ' '.join(self._commands) + ') ' + line
        else:
            yield ' '.join(self._commands)

    @property
    def output(self):
        logging.debug('Process out.')

        if type(self._exception) is subprocess.CalledProcessError:
            for line in self._exception.output:
                yield line
        elif self._exception:
            yield str(self._exception)
        else:
            try:
                for line in iter(self._process.stdout.readline, b''):

                    if line == '' and not self._process.poll() is None:
                        logging.debug('Process output done.')
                        break

                    yield line.strip()

            except Exception as e:
                self._exception = e
                return

    @property
    def returncode(self):
        if self._process:
            self._process.wait()
        if type(self._exception) is subprocess.CalledProcessError:
            r = self._exception.returncode
        elif self._exception:
            r = 1
        else:
            r = self._process.returncode
        logging.debug('Process return: ' + str(r))
        return r

    @property
    def error(self):
        if self._process:
            self._process.wait()
        logging.debug('Process error:  ' + str(self._exception))
        if self._exception:
            return [str(self._exception)]
        else:
            return None


def run(commands, stdin=None):

    r = Process(commands, stdin).run()
    return r
