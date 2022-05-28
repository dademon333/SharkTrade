import os
from distutils.util import strtobool
from pathlib import Path


class Config:
    DEBUG = strtobool(os.getenv('DEBUG'))

    PROJECT_ROOT = Path(__file__).parent
    FRONT_ROOT = Path(PROJECT_ROOT.parent, 'frontend', 'build')

    MEDIA_ROOT = '/media'
    BACKUPS_ROOT = '/var/lib/postgres_backups'

    SERVER_URL = os.getenv('SERVER_URL')
