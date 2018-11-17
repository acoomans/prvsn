#!/usr/bin/env python3

import logging

from prvsnlib.provisioner import Provisioner


logging.basicConfig(format='%(message)s', level=logging.INFO)


# logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
# fileHandler = logging.FileHandler("{0}/{1}.log".format(logPath, fileName))
# fileHandler.setFormatter(logFormatter)
# rootLogger.addHandler(fileHandler)
# logging.getLogger().addHandler(logging.StreamHandler())


def main():
    print("hello main")
    runbook = '/Users/arnaud/src/prvsn/tests/runbook/'
    Provisioner(runbook, [
        'command'
    ]).run()

if __name__ == "__main__":
    main()