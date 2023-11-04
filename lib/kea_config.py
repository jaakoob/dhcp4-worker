import json
import logging

import requests


class KeaApi:

    def __init__(self, endpoint):
        self.endpoint = endpoint

    def get_kea_config(self) -> dict:
        data = {"command": "config-get", "service": ["dhcp4"]}
        r = requests.post(self.endpoint, data=json.dumps(data), headers={"Content-Type": "application/json"})
        if r.status_code == 200:
            config = r.json()[0]["arguments"]["Dhcp4"]
            config["reservations-global"]: True
            return config
        return {}

    def set_kea_config(self, config: dict) -> bool:
        data = {"command": "config-set", "service": ["dhcp4"], "arguments": {"Dhcp4": config}}
        r = requests.post(self.endpoint, data=json.dumps(data), headers={"Content-Type": "application/json"})
        if r.status_code == 200:
            if r.json()[0]["result"] == 0:
                logging.debug("Successfully set config")
                return True
            logging.error("Could not set kea config: %s" % (r.json()[0]["text"]))
            return False
        return False

    def write_kea_config(self, filename) -> bool:
        data = {"command": "config-write", "service": ["dhcp4"], "arguments": {"filename": filename}}
        r = requests.post(self.endpoint, data=json.dumps(data), headers={"Content-Type": "application/json"})
        logging.debug(r.text)
        if r.status_code == 200:
            if r.json()[0]["result"] == 0:
                logging.debug("Successfully wrote config")
                return True
            logging.error("Could not write kea config: %s" % (r.json()[0]["text"]))
            return False
        return False

    def reload_kea_config(self) -> bool:
        data = {"command": "config-reload", "service": ["dhcp4"]}
        r = requests.post(self.endpoint, data=json.dumps(data), headers={"Content-Type": "application/json"})
        if r.status_code == 200:
            if r.json()[0]["result"] == 0:
                logging.debug("Successfully reloaded config")
                return True
            logging.error("Could not reload kea config: %s" % (r.json()[0]["text"]))
            return False
        return False
