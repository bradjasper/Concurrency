import time
import simplejson as json

from twisted.internet import reactor
from twisted.internet import protocol
from twisted.internet import defer

from twisted.web import client
from txredis.protocol import Redis


@defer.inlineCallbacks
def main():

    clientCreator = protocol.ClientCreator(reactor, Redis)
    redis = yield clientCreator.connectTCP("184.72.238.148", 6379)

    while True:
        msg = yield redis.pop("redis_queue")

        if msg:
            print "message"
            data = json.loads(msg)

            @defer.inlineCallbacks
            def handle_response(response):
                num = yield redis.incr(str(data["test_name"]))
                print "Response done", num

            def handle_error(error):
                print "ERROR", error

            client.getPage(str(data["download_url"])).addCallbacks(
                callback=handle_response,
                errback=handle_error)


if __name__ == "__main__":
    reactor.callWhenRunning(main)
    reactor.run()
