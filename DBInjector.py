from pymongo.collection import Collection
from typing import Mapping, Any, List
from Logger import Logger


class DBInjector:
    def __init__(self, collection: Collection[Mapping[str, Any]], file_path: str, device_id: List,
                 logger: Logger = None) -> None:
        """
        The constructor that will create the dbInjector
        :param collection: The collection were we will put the data
        :param file_path: The file path that contains the data separated by ';'
        :param device_id: The name of the device that we will use
        :param logger: The logger that we will use for debug print
        """
        self.collection = collection
        self.file_path = file_path
        try:
            self.file = open(self.file_path, "r")
        except PermissionError as pe:
            logger.error_print(pe)
            exit(1)
        except FileNotFoundError as fnfe:
            logger.error_print(fnfe)
            exit(1)
        self.device_id = device_id
        self.logger = logger

    def inject_file_in_db(self):
        """
        Will read the whole file and input it inside the collection
        """
        line = self.file.readline()
        # remove space in the header
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
            if self.logger:
                self.logger.debug_print("Inserted : " + str(data))
