import redis
import json 
import urllib

db = redis.Redis()

while True:
    key, msg = db.blpop("redis_queue")
    data = json.loads(msg)
    db.incr(data["test_name"])

    print data["download_url"]
    url = urllib.urlopen(data["download_url"])
    print url.read()
    db.set("download_url", data["download_url"])
