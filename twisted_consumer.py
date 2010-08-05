"""
from twisted.internet import reactor
from twisted.web.client import getPage
from twisted.python.util import println
import sys

num = 200

def done():
    global num

    print "DONE", num
    num -= 1

    if num == 0:
        print "COMPLETELY FINISHED :)"
        reactor.stop()

def handle_response(response):
    print
    print
    print
    print
    print "RESPONSE"
    print
    print
    print
    print response
    done()

def handle_error(error):
    print "ERROR:", error
    done()

for x in xrange(num):
    getPage("http://www.google.com").addCallbacks(callback=handle_response, errback=handle_error)

reactor.run()

"""


from twisted.internet import reactor
from twisted.internet import protocol
from twisted.internet import defer

from txredis.protocol import Redis

# Hostname and Port number of a redis server
HOST = 'localhost'
PORT = 6379

@defer.inlineCallbacks
def main():
    clientCreator = protocol.ClientCreator(reactor, Redis)
    redis = yield clientCreator.connectTCP(HOST, PORT)
    
    res = yield redis.ping()
    print res

    info = yield redis.info()
    print info

    res = yield redis.set('test', 42)
    print res
    
    test = yield redis.get('test')
    print test

if __name__ == "__main__":
    main()
    reactor.run()

