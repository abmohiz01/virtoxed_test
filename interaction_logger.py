import logging
from datetime import datetime

def setup_logger():
    logger = logging.getLogger("InteractionLogger")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler(f"interaction_log_{datetime.now().strftime('%Y-%m-%d')}.log")
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
