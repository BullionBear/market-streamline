# log_config.py
import logging


def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Create handlers (e.g., StreamHandler, FileHandler)
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)

    # Create formatter and add it to handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(handler)
