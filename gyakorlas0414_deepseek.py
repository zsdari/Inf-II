import logging
from datetime import datetime
from typing import List, Optional

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y/%m/%d %H:%M:%S"
SUPPORTED_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']


class LogMan:
    def __init__(self, log_file: str = 'application.log'):
        self.log_file = log_file
        self.logger_name = f"LogMan_{log_file}"  # EZ HIÁNYZOTT!
        self._setup_logging()
        # self.logger = None  # EZT VEDD KI, mert a _setup_logging beállítja

    def _setup_logging(self):
        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(logging.DEBUG)

        # Fontos: ne adjunk hozzá többször handlert!
        if not self.logger.handlers:
            file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
            formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def write_log(self, level: str, msg: str):
        level = level.upper()

        # Az összes szintet kezeljük
        if level == "DEBUG":
            self.logger.debug(msg)
        elif level == "INFO":
            self.logger.info(msg)
        elif level == "WARNING":
            self.logger.warning(msg)
        elif level == "ERROR":
            self.logger.error(msg)
        elif level == "CRITICAL":
            self.logger.critical(msg)
        else:
            print(f"Ismeretlen szint: {level}")

    def read_logs(self, filter_levels: Optional[List[str]] = None):
        entries = []  # EZ HIÁNYZOTT!

        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if filter_levels:
                        # Ellenőrizzük, hogy a sor tartalmazza-e a keresett szintek valamelyikét
                        for szint in filter_levels:
                            if f" - {szint.upper()} - " in line:
                                entries.append(line.strip())
                                break
                    else:
                        entries.append(line.strip())
        except FileNotFoundError:
            print(f"A fájl még nem létezik: {self.log_file}")

        return entries

