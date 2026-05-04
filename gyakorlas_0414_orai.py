import logging
from datetime import datetime
from typing import List, Optional

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y/%m/%d %H:%M:%S"
SUPPORTED_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']


class LogMan:
    def __init__(self, log_file: str = 'application.log'):
        self.log_file = log_file
        self._logger = None
        self._setup_logging()

    def _setup_logging(self):
        self._logger = logging.getLogger(type(self).__name__)
        self._logger.setLevel(logging.DEBUG)
        self._handler = logging.FileHandler(self.log_file, encoding='utf-8')
        formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
        self._handler.setFormatter(formatter)
        self._logger.addHandler(self._handler)

    def write_log(self, level : str, msg : str):
        if level.upper() not in SUPPORTED_LEVELS:
            raise ValueError(f'Unsupported log level: {level}')
        numeric_level = getattr(logging, level.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % level)
        self._logger.log(numeric_level, msg)

    def read_log(self, filter_levels: Optional[List[str]] = None) -> List[str]:
        pass

if __name__ == '__main__':
    logger = LogMan()
    logger.write_log('INFO', 'Start app...')
    logger.write_log('ERROR', 'Task 1 error...')
    logger.write_log('DEBUG', 'Task 1 error handling...')