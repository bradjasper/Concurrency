import time
import random
import json

import redis

db = redis.Redis()

for num in [150, 150, 300, 300]:

    test_name = "concurrency_test_%d" % db.incr("concurrency_num_tests")
    urls = [
        "http://www.rentacarnow.com",
        "http://bradjasper.com"
    ]

    print "Running test %s at %d messages" % (test_name, num)

    start_time = time.time()

    for i in xrange(num):
        db.lpush("redis_queue", json.dumps({
            "download_url": random.choice(urls),
            "rate_id": "243234-234234234-234234234234-234234234234",
            "search_id": "234234234-234234234234-234234234-234234234",
            "test_name": test_name,
            "vendor": "hertz"}))

    print "Done publishing in %f seconds" % (time.time() - start_time)

    # Wait until 95% of results are done
    percentage = 0
    while percentage < 80:
        percentage = 100 * int(db.get(test_name) or 0) / num
        print "Completed %d%%..." % percentage
        time.sleep(.5)

    print "Done in %f seconds" % (time.time() - start_time)
