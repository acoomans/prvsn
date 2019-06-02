#!/usr/bin/python

import logging
import os
import tempfile
import shutil
import zipfile

from prvsnlib.provisioner import Provisioner
from prvsnlib.models import Runbook


def extract():
    d = tempfile.mkdtemp()
    logging.debug('Extracting package to %s' % d)
    archive = os.path.dirname(__file__)
    zf = zipfile.ZipFile(archive)
    zf.extractall(d)
    return d


def cleanup(d):
    logging.debug('Cleaning up %s' % d)
    shutil.rmtree(d)


def bootstrap(runbooks=[], loglevel=logging.INFO):
    logging.root.setLevel(loglevel)

    d = extract()
    Provisioner(
        runbooks=[Runbook(os.path.join(d, runbook)) for runbook in runbooks]
    ).run()
    cleanup(d)


if __name__ == "__main__":
    bootstrap(
        #ARGUMENTS#
    )
