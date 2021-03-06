import logging
import os
import sys


def log_error_and_exit(message):
    logging.error(message)
    sys.exit(1)


def validate_runbook(runbook):
    if not os.path.isdir(runbook.path):
        log_error_and_exit('Not a valid runbook: ' + runbook.path)
    return True


def validate_roles(runbook, roles):
    if not type(roles) is str:
        log_error_and_exit('Not valid roles: ' + roles)
    if not roles:
        log_error_and_exit('No roles specified. Nothing to do.')
    for role in roles.split(','):
        if role not in [r.name for r in runbook.roles]:
            log_error_and_exit('Not a valid role in runbook: ' + role)
    return True


def validate_username(username):
    if not username or not type(username) is str:
        log_error_and_exit('Not a valid username: ' + username)
    return True


def validate_hostname(hostname):
    if not hostname or not type(hostname) is str:
        log_error_and_exit('Not a valid hostname: ' + hostname)
    return True
