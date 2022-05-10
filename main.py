import pymongo
import json

#Client
client = pymongo.MongoClient()

#set the database name to rfid_data
self_rfid_database = client["SELF_RFID_DATA"]
other_rfid_database = client["OTHER_RFID_DATA"]

#create a collection of raw_data
self_raw_data = self_rfid_database["RAW_DATA"]
other_raw_data = other_rfid_database["RAW_DATA"]

#decode a json string to a dictionnary
string = '{"name" : "test"}'
data = json.loads(string)
print(data)

self_raw_data.drop()

#put the decoded data into the database and adapt it
self_raw_data.insert_one(data)

for data in self_raw_data.find():
    print(data)

client.close()