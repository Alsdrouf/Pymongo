import pymongo
from WebsocketManager import WebsocketManager
from Logger import Logger
from DBInjector import DBInjector
import json

DEBUG = True
try:
    config = open("conf.json", "r")
except PermissionError as pe:
    print("No permission to read on config file", pe)
    exit(1)
except FileNotFoundError as fnfe:
    print("File wasn't created")
    exit(1)

try:
    conf = json.load(config)
except json.JSONDecodeError as jsonDecodeError:
    print(jsonDecodeError.msg)
    exit(1)

DEVICE_ID = conf["device_id"]
logger = Logger("./log.txt", conf["DEBUG"])

#Client
client = pymongo.MongoClient(conf["server"]["address"], conf["server"]["port"])

#set the database name to rfid_data
self_rfid_database = client["SELF_RFID_DATA"]
other_rfid_database = client["OTHER_RFID_DATA"]

#create a collection of raw_data
self_raw_data = self_rfid_database["RAW_DATA"]
other_raw_data = other_rfid_database["RAW_DATA"]

websocketManager = WebsocketManager(self_raw_data, DEVICE_ID, logger)

#TODO read the real websocket here
#websocketManager.onIncomingMessage('{"timestamp": "2022-05-10 11:06:03+02:00", "RFID_status": "ON", "IR_status": {}, "Sensor": "", "Status": "Waiting a tag to read", "Alarm": "False", "bat_percent": 0, "bat_voltage": 0, "temperature_board": 0, "type": "information 279"}')

dbInjector = DBInjector(self_raw_data, "./BirdDevice18_220327.csv", DEVICE_ID, logger)
dbInjector.injectFileInDB()

for data in self_raw_data.find():
    logger.debugPrint(data)

client.close()