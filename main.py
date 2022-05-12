import time
import Util
from WebsocketManager import WebsocketManager
from Logger import Logger
from DBInjector import DBInjector
from typing import List
from DBManager import DBManager
from DBClient import DBClient

conf = Util.load_config()

DEBUG: bool = conf["DEBUG"]
DEVICE_ID: str = conf["device_id"]
DEVICE_LABEL: List[str] = conf["device_label"]
logger = Logger("./log.txt", DEBUG)

logger.info_print("script started successfully")

# Client
db_manager = DBManager(address=conf["server"]["address"], port=conf["server"]["port"], logger=logger)

if DEBUG:
    db_manager.drop_database("DATA")

db_client = DBClient(db_manager)
db_client.get_or_update_device(DEVICE_ID, DEVICE_LABEL)

websocketManager = WebsocketManager(db_client.database, DEVICE_ID, logger)

# TODO read the real websocket here

logger.info_print("Starting stress test of websocket")
startTime = time.time() * 1000
for i in range(10000):
    websocketManager.on_incoming_message(
        """
        {
            "timestamp": "2022-05-10 11:06:03.927+02:00",
            "Sensor": "A0",
            "Status": "3B0018BE3E",
            "Latitude": "",
            "Longitude": "",
            "Alarm": "False",
            "System": " ",
            "type": "record"
        }
        """
    )
endTime = time.time() * 1000
logger.info_print("Ended test of websocket stress test : took " + str(int(endTime - startTime)) + "ms")

logger.info_print("Starting test of db injector")
startTime = time.time() * 1000
dbInjector = DBInjector(db_client.database, "./BirdDevice18_220327.csv", DEVICE_ID, logger)
dbInjector.inject_file_in_db()
endTime = time.time() * 1000

logger.info_print("Ended test of db injector : took " + str(int(endTime - startTime)) + "ms")

for status in db_client.status_collection.find():
    logger.debug_print(status)

# Test of aggregation
result = db_client.database["DATA"].aggregate([
    {
        "$lookup": {
            "from": "DEVICES",
            "localField": "device_id",
            "foreignField": "_id",
            "as": "DEVICE_DATA"
        }
    },
    {"$unwind": "$DEVICE_DATA"},
    {
        "$lookup": {
            "from": "STATUS",
            "localField": "status",
            "foreignField": "_id",
            "as": "DEVICE_STATUS"
        }
    },
    {"$unwind": "$DEVICE_STATUS"},
    {
        "$lookup": {
            "from": "SENSORS",
            "localField": "sensor",
            "foreignField": "_id",
            "as": "DEVICE_SENSOR"
        }
    },
    {"$unwind": "$DEVICE_SENSOR"}
], allowDiskUse=True)

# Example of aggregation result
for res in result:
    logger.debug_print(res)

logger.info_print("script ended successfully")

db_client.close_connection()
