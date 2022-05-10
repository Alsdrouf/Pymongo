from pymongo.collection import Collection
from typing import Mapping, Any
from Logger import Logger

class DBInjector:
    def __init__(self, collection: Collection[Mapping[str, Any]], file_path: str, logger: Logger = None) -> None:
        self.collection = collection
        self.file_path = file_path
        self.file = open(self.file_path, "r")
        self.logger = logger

    def injectFileInDB(self):
        line = self.file.readline()
        #remove space in the header
        header = line.replace(" ", "").split(";")
        while True:
            line = self.file.readline()
            if not line:
                break
            content = line.split(";")
            data = {}
            i = 0
            for head in header:
                data[head] = content[i]
                i+=1
            self.collection.insert_one(data)
            self.logger.debugPrint("Inserted : " + str(data))
