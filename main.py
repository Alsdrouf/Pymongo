import pymongo
from WebsocketManager import WebsocketManager
from Logger import Logger

DEBUG = True
DEVICE_ID = ["BirdDevice18", "sbgacq18"]
logger = Logger("./log.txt")

#Client
client = pymongo.MongoClient()

#set the database name to rfid_data
self_rfid_database = client["SELF_RFID_DATA"]
other_rfid_database = client["OTHER_RFID_DATA"]

#create a collection of raw_data
self_raw_data = self_rfid_database["RAW_DATA"]
other_raw_data = other_rfid_database["RAW_DATA"]

websocketManager = WebsocketManager(self_raw_data, DEVICE_ID, logger)

#TODO learn the real websocket here
websocketManager.onIncomingMessage('{"timestamp": "2022-05-10 11:06:03+02:00", "RFID_status": "ON", "IR_status": {}, "Sensor": "", "Status": "Waiting a tag to read", "Alarm": "False", "bat_percent": 0, "bat_voltage": 0, "temperature_board": 0, "type": "information 279"}')

for data in self_raw_data.find():
    logger.debugPrint(data)

client.close()