import json
import os.path
from typing import Dict, Any, Mapping
from pymongo.collection import Collection
from pymongo.errors import PyMongoError


def load_config() -> Dict[str, Any]:
    """
    Function that will load a config file named conf.json
    :return: A dictionary with the config that was loaded
    """
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
    return conf


def insert_one_in_db_or_write_in_file(collection: Collection[Mapping[str, Any]], data: Dict[str, Any]) -> None:
    """
    Function that will try to insert the data in the collection and if there's an exception it will write it in the file
    :param collection: The collection to write data inside
    :param data: The data to write
    """
    try:
        collection.insert_one(data)
    except PyMongoError as pme:
        print(pme)
        write_in_file("backup.csv", data)
    except Exception as e:
        print(e)
        quit(1)


def write_in_file(file_path: str, data: Dict[str, any]) -> None:
    """
    Function that will write in a file the given data
    :param file_path: The file path to write inside
    :param data: The data to write
    """
    f = None
    has_header = os.path.isfile(file_path)
    try:
        f = open(file_path, "a+")
    except PermissionError as pe:
        # logger.error_print("No permission to write in the file")
        pass

    if not has_header:
        header = ""
        for key in data.keys():
            header += key + ";"

        header = header[:-1]

        f.write(header + "\n")

    content_str = ""
    for key in data:
        content_str += str(data[key])+";"

    content_str = content_str[:-1]
    print(content_str)

    f.write(content_str + "\n")
