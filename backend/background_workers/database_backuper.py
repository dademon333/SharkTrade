import os
import subprocess
import time
import traceback
from datetime import datetime
from pathlib import Path
from subprocess import DEVNULL, STDOUT

from config import Config
from tokens import Tokens


class DatabaseBackuper:
    """Automatically creates db backups every day in 00:00:10 and removes old."""

    @classmethod
    def init(cls):
        while True:
            try:
                # +10800 is GMT +3
                time.sleep(86400 - ((time.time() + 10800) % 86400) + 10)
                cls.create_backup()
                cls.remove_old_backups()
            except:
                traceback.print_exc()

    @classmethod
    def create_backup(cls) -> None:
        today = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        dump_location = Path(Config.BACKUPS_ROOT, f'{Tokens.POSTGRESQL_DATABASE}_{today}.sql')
        subprocess.call(
            f'pg_dump'
            f' {Tokens.DB_BACKUPER_POSTGRESQL_URL}'
            f' > {dump_location}',
            shell=True, stdout=DEVNULL, stderr=STDOUT
        )

    @classmethod
    def remove_old_backups(cls) -> None:
        to_remove = cls._get_old_backups()
        for backup_name in to_remove:
            os.remove(Path(Config.BACKUPS_ROOT, backup_name))

    @staticmethod
    def _get_old_backups() -> list[str]:
        backups = os.listdir(Config.BACKUPS_ROOT)
        to_remove = []

        for file_name in backups:
            try:
                created_at = datetime.strptime(
                    file_name.replace(f'{Tokens.POSTGRESQL_DATABASE}_', '').replace('.sql', ''),
                    '%Y-%m-%d_%H:%M:%S'
                )
            except:
                pass
            else:
                diff = datetime.now() - created_at
                # 90 days with error in 1000 seconds
                if diff.total_seconds() >= 90 * 86400 - 1000:
                    to_remove.append(file_name)

        return to_remove
