import os
import sys
from pathlib import Path

from dotenv import load_dotenv

if 'pytest' in sys.argv[0]:
    load_dotenv('../.env')


class Config:
    DEBUG = os.getenv('DEBUG') == 'True'

    PROJECT_ROOT = Path(__file__).parent
    FRONT_ROOT = '/frontend/build'
    MEDIA_ROOT = '/user_media'
    BACKUPS_ROOT = '/var/lib/postgres_backups'

    SERVER_URL = os.getenv('SERVER_URL')
    CORS_ALLOWED_ORIGINS_REGEX = r'https?://localhost:[0-9]{1,5}'
