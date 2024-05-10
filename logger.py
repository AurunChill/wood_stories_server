# Standard
import logging
import os

# Project
from config import BASE_PATH


class Logger:
    """A basic wrapper class for Python logger with custom methods to output logs to console and file"""

    def __init__(self, name, logging_path: str):
        """Initialize the Logger object.

        Args:
            name (str): The name of the logger instance.
            logging_path (str): The path to the log file to write logs to.
        """
        self.__logging_path = logging_path
        self.log = logging.getLogger(name)  # Unique logger per instance
        self.log.setLevel(logging.INFO)

        # Create file handler which logs messages to the specified file
        file_handler = logging.FileHandler(logging_path, encoding='utf-8')
        file_handler.setLevel(logging.INFO)

        # Create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                                      datefmt='%Y-%m-%d:%H:%M:%S')
        file_handler.setFormatter(formatter)

        # Add the handlers to the logger
        self.log.addHandler(file_handler)

    def clear_log_file(self):
        """Clear the content of the log file.

        Returns:
            str: An empty string indicating successful log file clearing.
        """
        if self.__logging_path:
            with open(self.__logging_path, "w") as f:
                f.write("")
            return ""

    def info(self, msg: str):
        """Log an information message.

        Args:
            msg (str): The message to log.
        """
        print(msg)  # Show in console
        self.log.info(msg)

    def warning(self, msg: str):
        """Log a warning message.

        Args:
            msg (str): The message to log.
        """
        print(msg)  # Show in console
        self.log.warning(msg)

    def error(self, msg: str):
        """Log an error message.

        Args:
            msg (str): The message to log.
        """
        print(msg)  # Show in console
        self.log.error(msg)


# Create a folder to store log files
logging_folder = BASE_PATH / 'logs'
if not os.path.exists(logging_folder):
    os.makedirs(logging_folder, exist_ok=True)

# Create a logger instance for GPT logs and specify the log file path
gpt_logger = Logger(name='gpt', logging_path=os.path.join(logging_folder, 'gpt_log.log'))

# Clear the contents of the log file before logging new information
gpt_logger.clear_log_file()