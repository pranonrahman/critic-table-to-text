import logging


def configure_logger(logger_name, log_level=logging.INFO):
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)

    logger.addHandler(handler)
