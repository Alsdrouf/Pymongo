import pymongo
from Logger import Logger
from typing import Any, Mapping, Union
from pymongo.database import Database
from pymongo.collection import Collection

class DBManager:
    def __init__(
            self,
            address: str = "localhost",
            port: int = 27017,
            server_selection_timeout_ms: int = 2000,
            logger: Logger = None
    ) -> None:
        """
        Constructor that will open the connection with the mongoDB server
        :param address: The address of the server
        :param port: The port of the server
        :param server_selection_timeout_ms: The time to try to connect before giving up
        :param logger: The logger that will be use in case of error, information or debug
        """
        self.server_address = address
        self.server_port = port

        self.client = pymongo.MongoClient(
            self.server_address,
            self.server_port,
            serverSelectionTimeoutMS=server_selection_timeout_ms
        )

        try:
            self.client.server_info()
        except pymongo.mongo_client.ServerSelectionTimeoutError as sste:
            if logger:
                logger.error_print(sste)
            exit(1)

    def get_database(self, database: str) -> Database[Mapping[str, Any]]:
        """
        Function that will return the requested database
        :param database: The requested database name
        :return: The database with the name given
        """
        return self.client[database]

    def get_collection_of_database(self, database: str, collection: str) -> Collection[Mapping[str, Any]]:
        """
        Function that will return the requested collection of the requested database
        :param database: The database name from where we will get the collection
        :param collection: The requested collection name
        :return: The collection from the database given
        """
        return self.get_database(database)[collection]

    def drop_database(self, database: str) -> None:
        """
        Function that delete the given database name
        :param database: The database name that will be deleted
        """
        self.client.drop_database(database)

    def close_connection(self) -> None:
        """
        Function that will close the connection with mongoDB
        """
        self.client.close()



