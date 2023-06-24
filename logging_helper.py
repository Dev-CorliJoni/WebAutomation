import logging
from logging.handlers import RotatingFileHandler


class CustomFormatter(logging.Formatter):

    GREY = "\x1b[38;20m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    BOLD_RED = "\x1b[31;1m"
    RESET = "\x1b[0m"

    SINGLE_LINE_MESSAGE_FORMAT = "[%(levelname)s] <%(filename)s - %(funcName)s() line %(lineno)s> -> %(message)s"
    MESSAGE_FORMAT = SINGLE_LINE_MESSAGE_FORMAT

    FORMATS = {
        logging.DEBUG:      lambda:   CustomFormatter.GREY +      CustomFormatter.MESSAGE_FORMAT + CustomFormatter.RESET,
        logging.INFO:       lambda:   CustomFormatter.GREY +      CustomFormatter.MESSAGE_FORMAT + CustomFormatter.RESET,
        logging.WARNING:    lambda:   CustomFormatter.YELLOW +    CustomFormatter.MESSAGE_FORMAT + CustomFormatter.RESET,
        logging.ERROR:      lambda:   CustomFormatter.RED +       CustomFormatter.MESSAGE_FORMAT + CustomFormatter.RESET,
        logging.CRITICAL:   lambda:   CustomFormatter.BOLD_RED +  CustomFormatter.MESSAGE_FORMAT + CustomFormatter.RESET
    }

    def format(self, record):
        if record.exc_info is not None:
            CustomFormatter.MESSAGE_FORMAT = "\n" + CustomFormatter.SINGLE_LINE_MESSAGE_FORMAT + "\n"
        else:
            CustomFormatter.MESSAGE_FORMAT = CustomFormatter.SINGLE_LINE_MESSAGE_FORMAT

        log_fmt = self.FORMATS.get(record.levelno)()
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_logger(name):
    _logger = logging.getLogger(name)
    _logger.setLevel(logging.DEBUG)

    _logger.addHandler(console_handler)
    _logger.addHandler(file_handler)
    return _logger


console_handler = logging.StreamHandler()
console_handler.setFormatter(CustomFormatter())
console_handler.setLevel(logging.INFO)

_format = "\n\n(%(asctime)s) [%(levelname)s] <%(filename)s - %(funcName)s() line %(lineno)s> -> %(message)s\n\n"
file_handler = RotatingFileHandler("Logs\log.log", maxBytes=50000, backupCount=5)
file_handler.setFormatter(logging.Formatter(_format))
file_handler.setLevel(logging.CRITICAL)
