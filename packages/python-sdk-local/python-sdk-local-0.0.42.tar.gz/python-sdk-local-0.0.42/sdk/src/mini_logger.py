import sys
from datetime import datetime


class MiniLogger:

    @staticmethod
    def start(message: str = "", object: dict = None):
        """
        Print a log message with the current time.

        Parameters:
            message (str): The message to be printed.
        """
        if object is None:
            print(f"{datetime.now()} - START - {message}")
        else:
            print(f"{datetime.now()} - START - {message} - {str(object)}")

    @staticmethod
    def end(message: str = "", object: dict = None):
        """
        Print a log message with the current time.

        Parameters:
            message (str): The message to be printed.
        """
        if object is None:
            print(f"{datetime.now()} - END - {message}")
        else:
            print(f"{datetime.now()} - END - {message} - {str(object)}")

    @staticmethod
    def info(message: str = "", object: dict = None):
        """
        Print a log message with the current time.

        Parameters:
            message (str): The message to be printed.
            object (dict): The object to be printed.
        """
        if object is None:
            print(f"{datetime.now()} - INFO - {message}")
        else:
            print(f"{datetime.now()} - INFO {message} - {str(object)}")

    @staticmethod
    def error(message: str = "", object: dict = None):
        """
        Print a log error message with the current time.

        Parameters:
            message (str): The message to be printed.
            object (dict): The object to be printed.
        """
        if object is None:
            print(f"{datetime.now()} - ERROR - {message}",
                  file=sys.stderr)
        else:
            print(
                f"{datetime.now()} - ERROR - {message} - {str(object)}", file=sys.stderr)
