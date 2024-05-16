import logging
import os

class Logger:
    r"""
    Initialize the Logger object.

    Args:
        log_file_name (str): The name of the log file.
        level (int, optional): The logging level. Defaults to logging.INFO.
    """
            
    def __init__(self, log_file_name, level=logging.INFO):

        self.logger = logging.getLogger(log_file_name)
        self.logger.setLevel(level)
        self.logger.propagate = False

        # Create a file handler that logs messages to a file
        if not os.path.exists('logs'):
            os.makedirs('logs')
        file_handler = logging.FileHandler(f'logs/{log_file_name}.log')

        # Create a formatter and set it for the handler
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Add the handler to the logger
        self.logger.addHandler(file_handler)

    def log(self, message, level=logging.INFO):
        if level == logging.DEBUG:
            self.logger.debug(message)
        elif level == logging.INFO:
            self.logger.info(message)
        elif level == logging.WARNING:
            self.logger.warning(message)
        elif level == logging.ERROR:
            self.logger.error(message)
        elif level == logging.CRITICAL:
            self.logger.critical(message)
        else:
            self.logger.info(message)



