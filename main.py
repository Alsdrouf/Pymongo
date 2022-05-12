import time
import DataPretierAndConverter
import Util
from WebsocketManager import WebsocketManager
from Logger import Logger
from DBInjector import DBInjector
from typing import List
from DBManager import DBManager

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

database = db_manager.get_database("DATA")

# create the collections
device_collection = database["DEVICES"]
if "device_id_1" not in device_collection.index_information():
    device_collection.create_index("device_id", unique=True)

sensor_collection = database["SENSORS"]
if "sensor_code_1" not in sensor_collection.index_information():
    sensor_collection.create_index("sensor_code", unique=True)

counter_collection = database["COUNTER"]
if counter_collection.count_documents({}) == 0:
    counter_collection.insert_one({"status_count": 0})
    counter_collection.insert_one({"sensor_count": 0})

status_collection = database["STATUS"]

DataPretierAndConverter.counter_collection = counter_collection
DataPretierAndConverter.sensor_collection = sensor_collection
DataPretierAndConverter.status_collection = status_collection

device = device_collection.find_one({"device_id": DEVICE_ID})
logger.debug_print(device)

if not device:
    device_collection.insert_one({"device_id": DEVICE_ID, "device_label": DEVICE_LABEL})
    logger.debug_print("Created new device entry in \"DEVICES\"")
elif device["device_label"] != DEVICE_LABEL:
    device_collection.update_one({"device_id": DEVICE_ID}, {"$set": {"device_label": DEVICE_LABEL}})
    logger.debug_print("Updating names of the device")

DEVICE_ID = device_collection.find_one({"device_id": DEVICE_ID})["_id"]

websocketManager = WebsocketManager(database, DEVICE_ID, logger)

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
dbInjector = DBInjector(database, "./BirdDevice18_220327.csv", DEVICE_ID, logger)
dbInjector.inject_file_in_db()
endTime = time.time() * 1000
logger.info_print("Ended test of db injector : took " + str(int(endTime - startTime)) + "ms")

for status in status_collection.find():
    logger.debug_print(status)

# Test of aggregation
result = database["DATA"].aggregate([
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

db_manager.close_connection()
