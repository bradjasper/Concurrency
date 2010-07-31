import time
import json

import redis

db = redis.Redis()
num = 100000

test_name = "concurrency_test_%d" % db.incr("concurrency_num_tests")

print "Running test %s at %d messages" % (test_name, num)

start_time = time.time()

for i in xrange(num):
    db.lpush("redis_queue", json.dumps({
        "download_url": "http://cnn.com/rss/edition.rss",
        "rate_id": "243234-234234234-234234234234-234234234234",
        "search_id": "234234234-234234234234-234234234-234234234",
        "test_name": test_name,
        "vendor": "hertz"}))

print "Done publishing in %f seconds" % (time.time() - start_time)

# Wait until all the results have been published
amount = 0
while amount != num:
    amount = int(db.get(test_name) or 0)

print "Done in %f seconds" % (time.time() - start_time)

db.del(test_name)
db.del("redis_queue")
