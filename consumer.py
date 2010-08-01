import redis
import json 
import urllib

import multiprocessing 

NUM_CONSUMERS = 25

db = redis.Redis(port=6378)

def consume():
    print "consuming..."
    while True:
        key, msg = db.blpop("redis_queue")
        data = json.loads(msg)

        download_url = data["download_url"]
        test_name = data["test_name"]

        url = urllib.urlopen(download_url)
        print url.read()
        db.set("download_url", download_url)

        db.incr(test_name)


for i in xrange(NUM_CONSUMERS):
    p = multiprocessing.Process(target=consume)
    p.start()
