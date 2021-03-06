import getpass
import logging


from prvsnlib.utils.run import Run


class CommandAction:
    RUN = 'run'


def command(interpreter, commands, user=None, ignore_errors=False, action=CommandAction.RUN):
    if action == CommandAction.RUN:
        logging.header('Run ' + interpreter[0])

        return Run(interpreter, stdin=commands, user=user, ignore_errors=ignore_errors).run()

    else:
        raise Exception('Invalid action')


def bash(*args, **kwargs):
    return command(['bash', '-e'], *args, **kwargs)


def ruby(*args, **kwargs):
    return command(['ruby'], *args, **kwargs)
