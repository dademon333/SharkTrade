import asyncio
import signal
import threading

from .database_backuper import DatabaseBackuper
from .online_updater import OnlineUpdater


async def run_daemons():
    threading.Thread(target=DatabaseBackuper.init, daemon=True).start()
    threading.Thread(target=asyncio.run, args=(OnlineUpdater().run(),), daemon=True).start()

    signal.signal(signal.SIGTERM, lambda: ...)
    signal.pause()


asyncio.run(run_daemons())
