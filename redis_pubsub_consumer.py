import redis
import json 

db = redis.Redis()
db2 = redis.Redis()

db.subscribe("redis_pubsub")

for msg in db.listen():
    if isinstance(msg["data"], basestring):
        data = json.loads(msg["data"])
        db2.incr(data["test_name"])
