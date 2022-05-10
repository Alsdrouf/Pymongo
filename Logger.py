from datetime import datetime

class Logger:
    def __init__(self, file_path: str, debug: bool = False) -> None:
        self.file_path = file_path
        self.file = open(self.file_path, "a+")
        self.debug = debug

    def debugPrint(self, message: str) -> None:
        if self.debug:
            self.writeToLog("[DEBUG]", message)

    def infoPrint(self, message: str) -> None:
        self.writeToLog("[INFO]", message)

    def errorPrint(self, message: str) -> None:
        self.writeToLog("[ERROR]", message)

    def writeToLog(self, prefix: str, message: str):
        self.file.write(datetime.now().isoformat() + " " + str(prefix) + " " + str(message) + "\n")
        print(datetime.now().isoformat(), prefix, message)