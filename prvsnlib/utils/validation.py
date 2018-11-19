import logging
import os
import sys

from prvsnlib.runbook import Runbook


def log_error_and_exit(message):
    logging.error(message)
    sys.exit(1)


def validate_runbook(runbook):
    if not type(runbook) is Runbook:
        log_error_and_exit('Argument runbook is not a valid Runbook.')
    if not os.path.isdir(runbook._path):
        log_error_and_exit('Argument "' + runbook._path + '" is not a valid runbook path.')
    return True


def validate_roles(runbook, roles):
    if not type(runbook) is Runbook:
        log_error_and_exit('Argument runbook is not a valid Runbook.')
    if not type(roles) is str:
        log_error_and_exit('Argument "' + roles + '" is not a valid roles list.')
    if not roles:
        log_error_and_exit('No roles specified. Nothing to do.')
    for role in roles.split(','):
        if role not in [r.name for r in runbook.roles]:
            log_error_and_exit('Argument "' + role + '" is not a valid role in runbook.')
    return True