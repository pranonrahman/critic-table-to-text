import logging

import coloredlogs

from src.configs import APPLICATION_NAME, LOG_LEVEL


def get_logger():
    logger = logging.getLogger(APPLICATION_NAME)
    coloredlogs.install(level=LOG_LEVEL, logger=logger, fmt='%(asctime)s %(levelname)s %(message)s')

    return logger

