import os
from distutils.util import strtobool


class Config:
    DEBUG = strtobool(os.getenv('DEBUG'))

    FRONT_ROOT = '/usr/src/frontend/build'
    BACKUPS_FOLDER = '/var/lib/postgres_backups'
