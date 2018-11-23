import getpass
import logging


from prvsnlib.utils.run import Run


class CommandAction:
    RUN = 'run'


def command(interpreter, commands, user=None, action=CommandAction.RUN):
    if action == CommandAction.RUN:
        logging.header('Run ' + interpreter[0])

        user_cmd = []

        if type(user) is str and user != getpass.getuser():
            user_cmd = ['sudo', '-u', user]

        return Run(user_cmd + interpreter, stdin=commands).run()

    else:
        raise Exception('Invalid action')


def bash(*args, **kwargs):
    return command(['bash', '-e'], *args, **kwargs)


def ruby(*args, **kwargs):
    return command(['ruby'], *args, **kwargs)
