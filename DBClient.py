from typing import List

import DataPretierAndConverter
from DBManager import DBManager
from Logger import Logger
from pymongo.collection import ObjectId


class DBClient:
    def __init__(self, db_manager: DBManager, logger: Logger = None) -> None:
        """
        Constructor that will create or get main database and create the index of them
        :param db_manager: The db_manager that will be used
        :param logger: The logger that will be used
        """
        self.db_manager = db_manager
        self.logger = logger

        self.database = self.db_manager.get_database("DATA")

        self.data_collection = self.database["DATA"]

        # create the collections
        self.device_collection = self.database["DEVICES"]
        if "device_id_1" not in self.device_collection.index_information():
            self.device_collection.create_index("device_id", unique=True)

        self.sensor_collection = self.database["SENSORS"]
        if "sensor_code_1" not in self.sensor_collection.index_information():
            self.sensor_collection.create_index("sensor_code", unique=True)

        self.counter_collection = self.database["COUNTER"]
        if self.counter_collection.count_documents({}) == 0:
            self.counter_collection.insert_one({"status_count": 0})
            self.counter_collection.insert_one({"sensor_count": 0})

        self.status_collection = self.database["STATUS"]

        DataPretierAndConverter.counter_collection = self.counter_collection
        DataPretierAndConverter.sensor_collection = self.sensor_collection
        DataPretierAndConverter.status_collection = self.status_collection

    def get_or_update_device(self, device_id: str, device_label: List[str]) -> ObjectId:
        """
        Function that will get or update the device label, and it will get the device id
        :param device_id: The device_id to get or update
        :param device_label: The list of label that can have the device
        :return: The _id of the device (take less storage)
        """
        device = self.device_collection.find_one({"device_id": device_id})
        if self.logger:
            self.logger.debug_print(device)

        if not device:
            self.device_collection.insert_one({"device_id": device_id, "device_label": device_label})
            if self.logger:
                self.logger.debug_print("Created new device entry in \"DEVICES\"")
        elif device["device_label"] != device_label:
            self.device_collection.update_one({"device_id": device_id}, {"$set": {"device_label": device_label}})
            if self.logger:
                self.logger.debug_print("Updating names of the device")

        return self.device_collection.find_one({"device_id": device_id})["_id"]

    def close_connection(self):
        """
        Function that will close the connection to the mongoDB server
        """
        self.db_manager.close_connection()


