from typing import Dict, Any, Mapping
from pymongo.collection import Collection

sensor_collection: Collection[Mapping[str, Any]] = None
counter_collection: Collection[Mapping[str, Any]] = None
status_collection: Collection[Mapping[str, Any]] = None
cache_status: Dict[str, Any] = {}
cache_sensor: Dict[str, Any] = {}
cache: Dict[str, Dict[str, Any]] = {}


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
    return get_id_of(sensor, "sensor_label", "_id", sensor_collection, counter_collection, "sensor_count")


def get_status_id_of_status(status: str) -> int:
    """
    Function that return the status id from status name
    :param status: The status name that we use to found the id
    :return: The status id that is found
    """
    return get_id_of(status, "status_label", "_id", status_collection, counter_collection, "status_count")


def get_id_of(
        something: Any,
        with_the_key: str,
        with_the_key_to_found: str,
        in_collection: Collection[Mapping[str, Any]],
        counter_col: Collection[Mapping[str, Any]],
        counter_name: str
) -> Any:
    """
    Function that will get a var in given table with a given search value,
    and it will add one with a counter if it's not exist
    :param something: The var to search (to simplify)
    :param with_the_key: The key to search in the given collection
    :param with_the_key_to_found: The key that will be returned from the collection
    :param in_collection: The collection to search in and return a var from
    :param counter_col: A collection that will contain an int at the given counter_name
    :param counter_name: The name of the counter that contains the int
    :return: The cached value that is found using all the information given
    """
    if with_the_key not in cache:
        cache[with_the_key] = {}
    cur_cache = cache[with_the_key]
    if something not in cur_cache:
        res = in_collection.find_one({with_the_key: something})
        if res:
            cur_cache[something] = res[with_the_key_to_found]
        else:
            id = None
            for count in counter_col.find():
                if counter_name in count:
                    id = count[counter_name] + 1
                    counter_col.update_one({"_id": count["_id"]}, {"$set": {counter_name: id}})
            in_collection.insert_one({"_id": id, with_the_key: something})
            cur_cache[something] = id
    return cur_cache[something]
