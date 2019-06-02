import datetime
import logging
import time


class Timer:

    def __init__(self):
        self.start()

    def start(self):
        self._start = time.time()

    def log_elapsed_time(self):
        delta = time.time() - self._start
        logging.info('Elapsed wall time clock: %d' % str(delta))
        return self
