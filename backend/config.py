import os
import sys
from distutils.util import strtobool
from pathlib import Path

from dotenv import load_dotenv

if 'pytest' in sys.argv[0]:
    load_dotenv('../.env')


class Config:
    DEBUG = strtobool(os.getenv('DEBUG'))

    PROJECT_ROOT = Path(__file__).parent
    FRONT_ROOT = Path(PROJECT_ROOT.parent, 'frontend', 'build')
    MEDIA_ROOT = '/user_media'
    BACKUPS_ROOT = '/var/lib/postgres_backups'

    SERVER_URL = os.getenv('SERVER_URL')
    CORS_ALLOWED_ORIGINS_REGEX = r'https?://localhost:[0-9]{1,5}'
