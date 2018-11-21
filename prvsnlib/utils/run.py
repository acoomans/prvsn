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
        self._process.wait()
        logging.debug('Process error:  ' + str(self._exception))
        if self._exception:
            return [str(self._exception)]
        else:
            return None



class Process2():

    def __init__(self, commands, stdin=None):
        self._commands = commands
        self._stdin_data = stdin
        self._returncode = None
        self._exception = None

    def run(self):
        logging.debug(self.__class__.__name__)

        try:

            stdin_read, stdin_write = os.pipe()
            stdout_read, stdout_write = os.pipe()

            logging.debug('Fork.')
            pid = os.fork()

            if pid == CHILD:
                try:
                    os.close(stdin_write)
                    os.close(stdout_read)

                    os.dup2(stdin_read, STDIN_FILENO)
                    os.dup2(stdout_write, STDOUT_FILENO)
                    os.dup2(stdout_write, STDERR_FILENO)

                    os.execv(self._commands[0], self._commands)
                except:
                    os.close(stdin_read)
                    os.close(stdout_write)
                    sys.exit(1)

            os.close(stdin_read)
            os.close(stdout_write)

            if self._stdin_data:
                logging.debug('Writing to stdin.')
                os.write(stdin_write, self._stdin_data.encode('utf-8'))
            os.close(stdin_write)

            self.pid = pid
            self.stdin_write = stdin_write
            self.stdout_read = stdout_read

        except Exception as e:
            print('yo2')
            self._exception = e
            return self

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

        pid = None

        if self._exception:
            yield str(self._exception)
        elif self.pid:
            try:
                with os.fdopen(self.stdout_read) as f:
                    while True:

                        line = f.readline()

                        # line = os.read(self.stdout_read, 1)
                        if line:
                            line = line.strip()
                            print(line)
                            yield line

                        try:
                            if pid is None:
                                pid, ret, res = os.wait4(-1, os.WNOHANG)
                                print(pid, ret)
                            if not line and pid:
                                logging.debug('Wait4 done.')
                                self._returncode = ret
                                break
                        except:
                            logging.debug('Exception during wait4.')
                            break

            except Exception as e:
                print('yo1')
                self._exception = e

    @property
    def returncode(self):

        pid, ret, res = os.wait4(-1, os.WNOHANG)
        print(pid, ret)

        print(str(self._exception))
        if self._exception:
            r = 1
        else:
            r = self._returncode
        logging.debug('Process return: ' + str(r))
        return r

    @property
    def error(self):

        pid, ret, res = os.wait4(-1, os.WNOHANG)
        print(pid, ret)

        logging.debug('Process error:  ' + str(self._exception))
        if self._exception:
            return str(self._exception)
        else:
            return None


def run(commands, stdin=None):

    r = Process(commands, stdin).run()
    # r = Process2(commands, stdin).run()
    return r
