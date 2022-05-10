from datetime import datetime


class Logger:
    def __init__(self, file_path: str, debug: bool = False) -> None:
        """
        The constructor of the logger
        :param file_path: The file path were the log will be put inside
        :param debug: True if debug message should be logged
        """
        self.file_path = file_path
        try:
            self.file = open(self.file_path, "a+")
        except PermissionError as pe:
            self.file = None
            self.error_print(pe)
            exit(1)
        self.debug = debug

    def debug_print(self, message: str) -> None:
        """
        A function that will print a debug message in the output 1> and in a file
        :param message: The message that will be written
        """
        if self.debug:
            self.write_to_log("[DEBUG]", message)

    def info_print(self, message: str) -> None:
        """
        A function that will print an info message in the output 1> and in a file
        :param message: The message that will be written
        """
        self.write_to_log("[INFO]", message)

    def error_print(self, message: str) -> None:
        """
        A function that will print an error message in the output 1> and in a file
        :param message: The message that will be written
        """
        self.write_to_log("[ERROR]", message)

    def write_to_log(self, prefix: str, message: str) -> None:
        """
        A function that will write a log like (time) (prefix) (message)
        :param prefix: The prefix that will be written in the log after the time
        :param message: The message that will be written after the prefix
        """
        if self.file:
            self.file.write(datetime.now().isoformat() + " " + str(prefix) + " " + str(message) + "\n")
        print(datetime.now().isoformat(), prefix, message)
