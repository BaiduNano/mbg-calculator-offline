import json
import os

CONFIG_FILE = "config.json"
DEFAULT_CONFIG = {
    "MBG_PER_DAY": 1.2e12,
    "USD_TO_IDR": 17400.0
}

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return DEFAULT_CONFIG
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
