from carrot.connection import BrokerConnection
from carrot.messaging import Consumer

import redis

conn = BrokerConnection(hostname="localhost", port=5672,
                         userid="guest", password="guest",
                         virtual_host="/")

consumer = Consumer(connection=conn, queue="feed",
              exchange="feed", routing_key="importer")

db = redis.Redis()

def message_callback(message_data, message):
    db.incr(message_data["test_name"])
    message.ack()
consumer.register_callback(message_callback)
consumer.wait()
