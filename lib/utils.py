import json
import jsonschema
import logging
from typing import Dict
import config as cfg


def parse_message(message: bytes) -> Dict:
    try:
        logging.debug("received message from rabbitmq: %s" % message)
        # try to read body from queue as json
        message = json.loads(message)
        
        # open json schema for coa message
        f = open(cfg.JSON_SCHEMA_PATH)
        schema = json.load(f)

        # validate body against schema
        jsonschema.validate(message, schema)

        result = dict()
        result["ip-address"] = message["ipv4Address"]
        result["hw-address"] = message["macAddress"]
        result["operation"] = message["operation"]

        return result
    except json.JSONDecodeError:
        logging.error("could not parse json from message queue")
        return None
    except jsonschema.exceptions.ValidationError:
        logging.error("message received from message queue does not fit supplied schema")
        return None
    except jsonschema.exceptions.SchemaError:
        logging.error("could not load schema")
        return None
