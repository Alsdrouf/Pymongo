from pymongo.collection import Collection, ObjectId
from typing import Mapping, Any

import DataPretierAndConverter
import Util
from Logger import Logger


class DBInjector:
    def __init__(self,
                 data_collection: Collection[Mapping[str, Any]],
                 file_path: str,
                 device_id: ObjectId,
                 logger: Logger = None) -> None:
        """
        The constructor that will create the dbInjector
        :param data_collection: The collection were we will put the data
        :param file_path: The file path that contains the data separated by ';'
        :param device_id: The name of the device that we will use
        :param logger: The logger that we will use for debug print
        """
        self.data_collection = data_collection
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
        header = line.lower().replace(" ", "")[:-1].split(";")
        for i in range(len(header)):
            if header[i] == "tracking":
                header[i] = "alarm"
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

            data["device_id"] = self.device_id
            sensor = data["sensor"]
            status = data["status"]

            if len(status) > 0:
                data["status"] = DataPretierAndConverter.get_status_id_of_status(status)
            if len(sensor) > 0:
                data["sensor"] = DataPretierAndConverter.get_sensor_id_of_sensor(sensor)
                Util.insert_one_in_db_or_write_in_file(self.data_collection, data)
                if self.logger:
                    self.logger.debug_print("Inserted : " + str(data))
