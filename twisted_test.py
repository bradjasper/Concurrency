from twisted.web import client
from twisted.internet import reactor

import time

num = 0


def do():

    df = client.getPage(url="https://www.rentacarnow.com/", followRedirect=True)

    def printOnError( error ):
        print "error"
        print 'E', error

    def printOnSuccess( page ):
        global num
        num += 1
        print "Got body", num

        if num == 100:
            reactor.stop()
            print "done"

    df.addErrback( printOnError )
    df.addCallback( printOnSuccess )

for x in range(100):
    reactor.callWhenRunning(do)

reactor.run()
