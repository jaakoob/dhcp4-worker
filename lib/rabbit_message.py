import json
import logging

import jsonschema
from jsonschema.validators import validate


def parse_message(message: bytes, schema_path: str):
    logging.debug(f"received message from rabbitmq: {message}")

    try:
        # try to read body from queue as json
        message = json.loads(message)

        # open json schema for coa message
        f = open(schema_path)
        schema = json.load(f)

        # validate body against schema
        validate(message, schema)

        lease = {
            "ip-address": message["ipv4Address"],
            "hw-address": message["macAddress"],
            "operation": message["operation"],
            "next-server": "0.0.0.0",
            "option-data": [],
            "boot-file-name": "",
            "client-classes": [],
            "hostname": message["ipv4Address"],
        }

    except json.JSONDecodeError as e:
        logging.error("could not decode message")
        return None
    except jsonschema.ValidationError as e:
        logging.error("message did not conform to supplied json schema")
        return None

    return lease
