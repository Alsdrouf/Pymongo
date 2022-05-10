from pymongo.collection import Collection
from typing import Mapping, Any, List
from Logger import Logger

class DBInjector:
    def __init__(self, collection: Collection[Mapping[str, Any]], file_path: str, device_id: List, logger: Logger = None) -> None:
        self.collection = collection
        self.file_path = file_path
        self.file = open(self.file_path, "r")
        self.device_id = device_id
        self.logger = logger

    def injectFileInDB(self):
        line = self.file.readline()
        #remove space in the header
        header = line.replace(" ", "")[:-1].split(";")
        while True:
            line = self.file.readline()
            if not line:
                break
            content = line.split(";")
            data = {}
            for i in range(len(header)):
                if i == len(header) - 1:
                    content[i] = content[i][:-1]
                data[header[i]] = content[i]

            data["Device_ID"] = self.device_id
            self.collection.insert_one(data)
            self.logger.debugPrint("Inserted : " + str(data))
