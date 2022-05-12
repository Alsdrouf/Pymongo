from typing import Dict, Any, Mapping
from pymongo.collection import Collection

sensor_collection: Collection[Mapping[str, Any]] = None
counter_collection: Collection[Mapping[str, Any]] = None
status_collection: Collection[Mapping[str, Any]] = None
cache_status: Dict[str, Any] = {}
cache_sensor: Dict[str, Any] = {}


def converter(data: Dict[str, Any]):
    pass


def join(data_one: Dict[str, Any], data_two: Dict[str, Any], on_one_key: str, on_two_key: str) -> Dict[str, Any]:
    pass


def get_sensor_id_of_sensor(sensor: str) -> int:
    """
    Function that return the sensor id from a sensor name
    :param sensor: The sensor name that we use to found the id
    :return: The sensor id that is found
    """
    if sensor not in cache_sensor:
        res = sensor_collection.find_one({"sensor_code": sensor})
        if res:
            cache_sensor[sensor] = res["sensor"]
        else:
            sensor_id = None
            for count in counter_collection.find():
                if "sensor_count" in count:
                    sensor_id = count["sensor_count"] + 1
                    counter_collection.update_one(
                        {"_id": count["_id"]},
                        {"$set": {"sensor_count": sensor_id}}
                    )
            sensor_collection.insert_one({"sensor": sensor_id, "sensor_code": sensor})
            cache_sensor[sensor] = sensor_id
    return cache_sensor[sensor]


def get_status_id_of_status(status: str) -> int:
    """
    Function that return the status id from status name
    :param status: The status name that we use to found the id
    :return: The status id that is found
    """
    if status not in cache_status:
        res = status_collection.find_one({"status_label": status})
        if res:
            cache_status[status] = res["status"]
        else:
            status_id = None
            for count in counter_collection.find():
                if "status_count" in count:
                    status_id = count["status_count"] + 1
                    counter_collection.update_one({"_id": count["_id"]}, {"$set": {"status_count": status_id}})
            status_collection.insert_one({"status": status_id, "status_label": status})
            cache_status[status] = status_id
    return cache_status[status]
