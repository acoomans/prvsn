import os

def real_user():
    if 'SUDO_USER' in os.environ.keys():
        return os.environ['SUDO_USER']
    else:
        return os.environ['USER']

def real_home():
    return os.environ['HOME']