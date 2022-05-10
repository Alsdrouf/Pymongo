import json

import pymongo
from pymongo.collection import Collection
from typing import Any, Mapping, Dict, List
from Logger import Logger

class WebsocketManager:
    def __init__(self, collection: Collection[Mapping[str, Any]], device_id: List, logger: Logger = None) -> None:
        self.collection = collection
        self.device_id = device_id
        self.logger = logger

    def onIncomingMessage(self, message: str) -> None:
        noError = True
        # decode a json string to a dictionnary
        try:
            data = json.loads(message)
            data["Device_ID"] = self.device_id
            if self.logger:
                self.logger.debugPrint(data)
        except json.JSONDecodeError as jsonDecodeError:
            if self.logger:
                self.logger.errorPrint(jsonDecodeError.msg)
                self.logger.errorPrint("Avoid inserting the value")
            noError = False

        if noError:
            self.insertDataIntoTheDatabase(data)

    def insertDataIntoTheDatabase(self, data: Dict) -> None:
        try:
            self.collection.insert_one(data)
        except pymongo.mongo_client.PyMongoError as pyMongoError:
            if self.logger:
                self.logger.errorPrint("Unexcepted error " + str(pyMongoError))
