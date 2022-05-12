import json


def load_config():
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