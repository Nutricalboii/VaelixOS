"""
Vaelix Logger — Unified timestamped logger for all modules.
"""

import logging
import os
from datetime import datetime

LOG_DIR = os.path.expanduser("~/.local/share/vaelix-control-center/logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, f"vcc_{datetime.now().strftime('%Y-%m-%d')}.log")


class VaelixLogger:
    def __init__(self):
        logging.basicConfig(
            filename=LOG_FILE,
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        self._logger = logging.getLogger("VaelixCC")

    def log(self, message: str):
        self._logger.info(message)

    def error(self, message: str):
        self._logger.error(message)
