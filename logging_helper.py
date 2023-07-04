import logging
from logging.handlers import RotatingFileHandler

class CustomFormatter(logging.Formatter):
    """
    Custom log formatter class with colored console output.
    """

    GREY = "\x1b[38;20m"     # ANSI escape sequence for grey color
    YELLOW = "\x1b[33;20m"   # ANSI escape sequence for yellow color
    RED = "\x1b[31;20m"      # ANSI escape sequence for red color
    BOLD_RED = "\x1b[31;1m"  # ANSI escape sequence for bold red color
    RESET = "\x1b[0m"        # ANSI escape sequence to reset color

    SINGLE_LINE_MESSAGE_FORMAT = "[%(levelname)s] <%(filename)s - %(funcName)s() line %(lineno)s> -> %(message)s"
    MESSAGE_FORMAT = SINGLE_LINE_MESSAGE_FORMAT

    FORMATS = {
        logging.DEBUG:      lambda: CustomFormatter.GREY + CustomFormatter.MESSAGE_FORMAT + CustomFormatter.RESET,
        logging.INFO:       lambda: CustomFormatter.GREY + CustomFormatter.MESSAGE_FORMAT + CustomFormatter.RESET,
        logging.WARNING:    lambda: CustomFormatter.YELLOW + CustomFormatter.MESSAGE_FORMAT + CustomFormatter.RESET,
        logging.ERROR:      lambda: CustomFormatter.RED + CustomFormatter.MESSAGE_FORMAT + CustomFormatter.RESET,
        logging.CRITICAL:   lambda: CustomFormatter.BOLD_RED + CustomFormatter.MESSAGE_FORMAT + CustomFormatter.RESET
    }

    def format(self, record):
        """
        Override the format method of the logging.Formatter class.
        Adjusts the message format based on the presence of exception information.
        """
        if record.exc_info is not None:
            # If exc_info is availale, add linebreaks
            CustomFormatter.MESSAGE_FORMAT = "\n" + CustomFormatter.SINGLE_LINE_MESSAGE_FORMAT + "\n"
        else:
            CustomFormatter.MESSAGE_FORMAT = CustomFormatter.SINGLE_LINE_MESSAGE_FORMAT

        log_fmt = self.FORMATS.get(record.levelno)()
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_logger(name):
    """
    Creates and configures a logger object with custom handlers and formatters.
    """
    _logger = logging.getLogger(name)
    _logger.setLevel(logging.DEBUG)

    _logger.addHandler(console_handler)
    _logger.addHandler(file_handler)
    return _logger

def close_logging():
    """
    Shuts down the logging system.
    """
    logging.shutdown()

console_handler = logging.StreamHandler()
console_handler.setFormatter(CustomFormatter())
console_handler.setLevel(logging.INFO)

_format = "\n\n(%(asctime)s) [%(levelname)s] <%(filename)s - %(funcName)s() line %(lineno)s> -> %(message)s\n\n"
file_handler = RotatingFileHandler("Logs\log.log", maxBytes=50000, backupCount=5)
file_handler.setFormatter(logging.Formatter(_format))
file_handler.setLevel(logging.CRITICAL)
