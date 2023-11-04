import json
import logging


def parse_message(message: bytes):
    logging.debug(f"received message from rabbitmq: {message}")
    leases = list()

    try:
        # try to read body from queue as json
        message = json.loads(message)

        if len(message) == 1:
            for lease in message:
                leases.append({
                    "ip-address": lease["ipv4Address"],
                    "hw-address": lease["macAddress"],
                    "operation": lease["operation"],
                    "next-server": "0.0.0.0",
                    "option-data": [],
                    "boot-file-name": "",
                    "client-classes": [],
                    "hostname": lease["ipv4Address"],
                })
        else:
            for lease in message:
                leases.append({
                    "ip-address": lease["ipv4Address"],
                    "hw-address": lease["macAddress"],
                    "next-server": "0.0.0.0",
                    "option-data": [],
                    "boot-file-name": "",
                    "client-classes": [],
                    "hostname": lease["ipv4Address"],
                })

    except json.JSONDecodeError as e:
        logging.error("could not decode message")
        return None

    return leases
