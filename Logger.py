from datetime import datetime

class Logger:
    def __init__(self, file_path: str, debug: bool = False) -> None:
        self.file_path = file_path
        try:
            self.file = open(self.file_path, "a+")
        except PermissionError as pe:
            self.file = None
            self.errorPrint(pe)
            exit(1)
        self.debug = debug

    def debugPrint(self, message: str) -> None:
        if self.debug:
            self.writeToLog("[DEBUG]", message)

    def infoPrint(self, message: str) -> None:
        self.writeToLog("[INFO]", message)

    def errorPrint(self, message: str) -> None:
        self.writeToLog("[ERROR]", message)

    def writeToLog(self, prefix: str, message: str):
        if self.file:
            self.file.write(datetime.now().isoformat() + " " + str(prefix) + " " + str(message) + "\n")
        print(datetime.now().isoformat(), prefix, message)