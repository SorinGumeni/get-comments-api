import sys
from loguru import logger
import logging

from config import get_environment_config


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        log = logger.bind()

        log.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

def setup_logging():
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(get_environment_config().log_level)

    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    logger.configure(
        handlers=[
            {
                "sink": sys.stdout,
                "serialize": get_environment_config().serialize_logs,
                "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> <level>{level: <8}</level>"
                "- <cyan>{name}</cyan>:<cyan>{function}</cyan> - "
                "<level>{message}</level> ",
            }
        ]
    )