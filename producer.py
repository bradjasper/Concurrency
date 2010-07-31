import time

from carrot.connection import BrokerConnection
from carrot.messaging import Publisher

import redis

db = redis.Redis()
conn = BrokerConnection(hostname="localhost", port=5672,
                         userid="guest", password="guest",
                         virtual_host="/")
publisher = Publisher(connection=conn,
                      exchange="feed", routing_key="importer")
num = 9000

test_name = "concurrency_test_%d" % db.incr("concurrency_num_tests")

print "Running test %s at %d messages" % (test_name, num)

start_time = time.time()

for i in xrange(num):
    publisher.send({
        "download_url": "http://cnn.com/rss/edition.rss",
        "rate_id": "243234-234234234-234234234234-234234234234",
        "search_id": "234234234-234234234234-234234234-234234234",
        "test_name": test_name,
        "vendor": "hertz"})

publisher.close()

print "Done publishing"

# Wait until all the results have been published
amount = 0
while amount != num:
    amount = int(db.get(test_name))

print "Done in %f seconds" % (time.time() - start_time)
