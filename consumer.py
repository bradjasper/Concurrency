import time
import redis
import json 
import urllib

import multiprocessing 

NUM_CONSUMERS = 50

db = redis.Redis()

def consume():
    print "consuming..."
    while True:
        key, msg = db.blpop("redis_queue")
        data = json.loads(msg)

        download_url = data["download_url"]
        test_name = data["test_name"]

        print "downloading"
        url = urllib.urlopen(download_url)
        contents = url.read()
        print "downloaded"

        db.incr(test_name)

        time.sleep(0.1)


for i in xrange(NUM_CONSUMERS):
    p = multiprocessing.Process(target=consume)
    p.start()
