import json

import pymongo
from pymongo.database import Database
from typing import Any, Mapping, Dict

import DataPretierAndConverter
from Logger import Logger


class WebsocketManager:
    def __init__(self, database: Database[Mapping[str, Any]], device_id: str, logger: Logger = None) -> None:
        """
        The constructor that will create the websocket manager
        :param database: The database that will be used to put data inside
        :param device_id: A list that will contain all the device_name / id
        :param logger: The logger that will be used to make debug_print
        """
        self.database = database
        self.data = database["DATA"]
        self.sensor_collection = database["SENSORS"]
        self.device_id = device_id
        self.logger = logger

    def on_incoming_message(self, message: str) -> None:
        """
        A function that will treat received message that is a json string
        :param message: A valid json string that will be injected in the database
        """
        no_error = True
        # decode a json string to a dictionary
        data = None
        try:
            data: Dict[str, Any] = json.loads(message)
            newData = {}
            for key in data.keys():
                if key != key.lower():
                    newData[key.lower()] = data[key]
            data = newData
            data["device_id"] = self.device_id
            if self.logger:
                self.logger.debug_print(data)
        except json.JSONDecodeError as jsonDecodeError:
            if self.logger:
                self.logger.error_print(jsonDecodeError.msg)
                self.logger.error_print("Avoid inserting the value")
            no_error = False

        if no_error:
            status = data["status"]
            sensor = data["sensor"]
            if len(status) > 0:
                data["status"] = DataPretierAndConverter.get_status_id_of_status(status)
            if len(sensor) > 0:
                data["sensor"] = DataPretierAndConverter.get_sensor_id_of_sensor(sensor)
                self.data.insert_one(data)
            self.insert_data_into_the_database(data)

    def insert_data_into_the_database(self, data: Dict) -> None:
        """
        A function that will insert data into the database from a dictionary
        :param data: The dictionary that will be inserted in the database
        """
        try:
            self.data.insert_one(data)
        except pymongo.mongo_client.PyMongoError as pyMongoError:
            if self.logger:
                self.logger.error_print("Unexpected error " + str(pyMongoError))
