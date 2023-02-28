import json
import logging
from logging.handlers import SysLogHandler
from prometheus_client import start_http_server, Counter
import random
import ssl
import subprocess
from jsonschema import validate
import jsonschema
import pika
import config as cfg
from lib.utils import parse_message


def update_dhcp(ch: pika.channel.Channel, method_frame: pika.spec.Basic.Deliver, header_frame: pika.spec.BasicProperties, body: bytes) -> bool:
    attribs = parse_message(body)
    print(attribs)
    return True
 


def main():
    logger = logging.getLogger()
    #logger.addHandler(SysLogHandler(address = '/dev/log'))
    logger.setLevel(logging.INFO)

    start_http_server(9765)

    while(True):
        try:
            logging.debug("Connecting...")
            ## Shuffle the hosts list before reconnecting.
            ## This can help balance connections.
            random.shuffle(cfg.RABBITMQ_SERVER)
            con = pika.BlockingConnection(pika.ConnectionParameters(host=cfg.RABBITMQ_SERVER[0],
                                                                    port=cfg.RABBITMQ_PORT,
                                                                    virtual_host='/',
                                                                    ssl_options=pika.SSLOptions(context=ssl.create_default_context()),
                                                                    credentials=pika.PlainCredentials(cfg.RABBITMQ_USERNAME, cfg.RABBITMQ_PASSWORD)))
            ch = con.channel()
            ch.basic_consume(queue=cfg.RABBITMQ_QUEUE_NAME, on_message_callback=update_dhcp, auto_ack=True)
            logging.debug("bound to rabbitmq channel")
            try:
                ch.start_consuming()
            except (KeyboardInterrupt, SystemExit):
                ch.stop_consuming()
                ch.close()
                break
        except pika.exceptions.ConnectionClosedByBroker:
            logging.warning("AQMP connection was closed by a broker, retrying...")
            RABBIT_RECONNECTS.inc()
            continue
        # Do not recover on channel errors
        except pika.exceptions.AMQPChannelError as err:
            logging.error("Caught a channel error: {}, stopping...".format(err))
            break
        # Recover on all other connection errors
        except pika.exceptions.AMQPConnectionError:
            RABBIT_RECONNECTS.inc()
            logging.warning("AMQP Connection was closed, retrying...")
            continue


if __name__ == "__main__":
    main()
