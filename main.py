import sys
import time

import pymongo

import DataPretierAndConverter
from WebsocketManager import WebsocketManager
from Logger import Logger
from DBInjector import DBInjector
from typing import List
import json

config = None
try:
    config = open("conf.json", "r")
except PermissionError as pe:
    print("No permission to read on config file", pe)
    exit(1)
except FileNotFoundError as fnfe:
    print("Config file wasn't found", fnfe)
    exit(1)

conf = None
try:
    conf = json.load(config)
except json.JSONDecodeError as jsonDecodeError:
    print(jsonDecodeError.msg)
    exit(1)

DEBUG: bool = conf["DEBUG"]
DEVICE_ID: str = conf["device_id"]
DEVICE_LABEL: List[str] = conf["device_label"]
logger = Logger("./log.txt", DEBUG)

logger.info_print("script started successfully")

# Client
client = pymongo.MongoClient(conf["server"]["address"], conf["server"]["port"], serverSelectionTimeoutMS=2000)

try:
    client.server_info()
except pymongo.mongo_client.ServerSelectionTimeoutError as sste:
    logger.error_print(sste)
    exit(1)

# set the database name to DATA
database = client["DATA"]

if DEBUG:
    client.drop_database(database)

# create a collection of raw_data
device_collection = database["DEVICES"]
if "device_id_1" not in device_collection.index_information():
    device_collection.create_index("device_id", unique=True)

sensor_collection = database["SENSORS"]
if "sensor_id_1" not in sensor_collection.index_information():
    sensor_collection.create_index("sensor", unique=True)
    sensor_collection.create_index("sensor_code", unique=True)

counter_collection = database["COUNTER"]
if counter_collection.count_documents({}) == 0:
    counter_collection.insert_one({"status_count": 0})
    counter_collection.insert_one({"sensor_count": 0})

status_collection = database["STATUS"]
if "status_1" not in status_collection.index_information():
    status_collection.create_index("status", unique=True)

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
    websocketManager.on_incoming_message('{"timestamp": "2022-05-10 11:06:03+02:00", "RFID_status": "ON", "IR_status": {}, "Sensor": "", "Status": "Waiting a tag to read", "Alarm": "False", "bat_percent": 0, "bat_voltage": 0, "temperature_board": 0, "type": "information 279"}')
endTime = time.time() * 1000
logger.info_print("Ended test of websocket stress test : took " + str(int(endTime - startTime)) + "ms")


logger.info_print("Starting test of db injector")
startTime = time.time() * 1000
dbInjector = DBInjector(database, "./BirdDevice18_220327.csv", DEVICE_ID, logger)
dbInjector.inject_file_in_db()
endTime = time.time() * 1000
logger.info_print("Ended test of db injector : took " + str(int(endTime - startTime)) + "ms")

for status in status_collection.find():
    print(status)

logger.info_print("script ended successfully")

client.close()
