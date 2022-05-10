import json

import pymongo
from pymongo.collection import Collection
from typing import Any, Mapping, Dict, List
from Logger import Logger


class WebsocketManager:
    def __init__(self, collection: Collection[Mapping[str, Any]], device_id: List, logger: Logger = None) -> None:
        """
        The constructor that will create the websocket manager
        :param collection: The collection that will be used to put data inside
        :param device_id: A list that will contains all the device_name / id
        :param logger: The logger that will be used to make debug_print
        """
        self.collection = collection
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
            data = json.loads(message)
            data["Device_ID"] = self.device_id
            if self.logger:
                self.logger.debug_print(data)
        except json.JSONDecodeError as jsonDecodeError:
            if self.logger:
                self.logger.error_print(jsonDecodeError.msg)
                self.logger.error_print("Avoid inserting the value")
            no_error = False

        if no_error:
            self.insert_data_into_the_database(data)

    def insert_data_into_the_database(self, data: Dict) -> None:
        """
        A function that will insert data into the database from a dictionary
        :param data: The dictionary that will be inserted in the database
        """
        try:
            self.collection.insert_one(data)
        except pymongo.mongo_client.PyMongoError as pyMongoError:
            if self.logger:
                self.logger.error_print("Unexpected error " + str(pyMongoError))
