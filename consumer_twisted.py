from twisted.internet import reactor
from twisted.web.client import Agent
from twisted.web.http_headers import Headers
from twisted.internet.defer import Deferred
from twisted.internet.protocol import Protocol


class BeginningPrinter(Protocol):
    def __init__(self, finished):
        self.finished = finished
        self.remaining = 1024 * 10

    def dataReceived(self, bytes):
        if self.remaining:
            display = bytes[:self.remaining]
            print 'Some data received:'
            print display
            self.remaining -= len(display)

    def connectionLost(self, reason):
        print 'Finished receiving body:', reason.getErrorMessage()
        self.finished.callback(None)


def handle_response(response):
    print 'Response received', response
    finished = Deferred()
    response.deliverBody(BeginningPrinter(finished))
    return finished

def handle_shutdown(ignored):
    print "Shutdown"
    pass
    #reactor.stop()


agent = Agent(reactor)

d = agent.request(
    'GET',
    'http://www.google.com/',
    Headers({'User-Agent': ['Twisted Web Client Example']}),
    None)
d.addCallback(handle_response)
d.addBoth(handle_shutdown)


reactor.run()

