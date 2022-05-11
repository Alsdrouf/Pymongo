# Pymongo

## Prerequisite
- Python v3.8+
- Install requirements `python3 -m pip install -r requirements.txt`
- Install mongod and run it while the script is running

## Installation
- Rename the "default_conf.json" to "conf.json" `mv default_conf.json conf.json` or `cp default_conf.json conf.json`
- Config the file conf.json with your mongoDB server address and port and the id the current computer will have and if debug mode is enabled
- Make sure your mongoDB server is running and start the script `python3 main.py`
