import redis
import json 

db = redis.Redis()

while True:
    key, msg = db.blpop("redis_queue")
    data = json.loads(msg)
    db.incr(data["test_name"])
