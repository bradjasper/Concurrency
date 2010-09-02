import time
import random
import json
import sys

import redis

db = redis.Redis()

nums = map(int, sys.argv[1::])
assert nums, "No nums"

total_times = []

for num in nums:

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

    total_time = time.time() - start_time
    total_times.append(total_time)
    print "Done in %f seconds" % total_time

for num, total_time in zip(nums, total_times):
    print "Processed %d messages in %f seconds" % (num, total_time)
print "Average: %f seconds" % (sum(total_times) / len(total_times))
