import logging
from logging.handlers import RotatingFileHandler

def get_logger(name):
    _logger = logging.getLogger(name)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(CustomFormatter())
    console_handler.setLevel(logging.INFO)

    file_handler = RotatingFileHandler("Logs\log.log", maxBytes=50000, backupCount=5, delay=True)
    file_handler.setFormatter(logging.Formatter("\n\n(%(asctime)s) [%(levelname)s] <%(filename)s - %(funcName)s() line %(lineno)s> -> %(message)s\n\n"))
    file_handler.setLevel(logging.INFO)

    _logger.addHandler(console_handler)
    _logger.addHandler(file_handler)

    return _logger


class CustomFormatter(logging.Formatter):

    GREY = "\x1b[38;20m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    BOLD_RED = "\x1b[31;1m"
    RESET = "\x1b[0m"

    MESSAGE_FORMAT = "[%(levelname)s] <%(filename)s - %(funcName)s() line %(lineno)s> -> %(message)s\n"

    FORMATS = {
        logging.DEBUG: GREY + MESSAGE_FORMAT + RESET,
        logging.INFO: GREY + MESSAGE_FORMAT + RESET,
        logging.WARNING: YELLOW + MESSAGE_FORMAT + RESET,
        logging.ERROR: RED + MESSAGE_FORMAT + RESET,
        logging.CRITICAL: BOLD_RED + MESSAGE_FORMAT + RESET
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
