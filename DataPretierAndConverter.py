from typing import Dict, Any, Mapping
from pymongo.collection import Collection

sensor_collection: Collection[Mapping[str, Any]] = None
counter_collection: Collection[Mapping[str, Any]] = None
status_collection: Collection[Mapping[str, Any]] = None


def converter(data: Dict[str, Any]):
    pass


def get_sensor_id_of_sensor(sensor):
    if not sensor_collection.find_one({"sensor_code": sensor}):
        sensor_id = None
        for count in counter_collection.find():
            if "sensor_count" in count:
                sensor_id = count["sensor_count"] + 1
                counter_collection.update_one(
                    {"_id": count["_id"]},
                    {"$set": {"sensor_count": sensor_id}}
                )
        sensor_collection.insert_one({"sensor": sensor_id, "sensor_code": sensor})
    sensor_id = sensor_collection.find_one({"sensor_code": sensor})["sensor"]
    return sensor_id


def get_status_id_of_status(status):
    if not status_collection.find_one({"status_label": status}):
        status_id = None
        for count in counter_collection.find():
            if "status_count" in count:
                status_id = count["status_count"] + 1
                counter_collection.update_one({"_id": count["_id"]}, {"$set": {"status_count": status_id}})
        status_collection.insert_one({"status": status_id, "status_label": status})
    status_id = status_collection.find_one({"status_label": status})["status"]
    return status_id
