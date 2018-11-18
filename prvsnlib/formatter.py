import logging

from prvsnlib.utils.colors import Colors


# https://docs.python.org/3/library/logging.html#logging-levels

class LoggingLevels:
    HEADER = 25

logging.addLevelName(LoggingLevels.HEADER, 'Header')

def header(message, *args, **kwargs):
    logging.log(LoggingLevels.HEADER, message, *args, **kwargs)

logging.header = header


class Formatter(logging.Formatter):

    def format(self, record):
        res = super(Formatter, self).format(record)

        if record.levelno == logging.NOTSET:
            pass
        elif record.levelno == logging.DEBUG:
            pass
        elif record.levelno == logging.INFO:
            pass
        elif record.levelno == LoggingLevels.HEADER:
            res = Colors.HEADER + '# ' + res + Colors.END
        elif record.levelno == logging.WARNING:
            res = Colors.WARNING + res + Colors.END
        elif record.levelno == logging.ERROR:
            res = Colors.ERROR + res + Colors.END
        elif record.levelno == logging.CRITICAL:
            res = Colors.ERROR + res + Colors.END
        return res