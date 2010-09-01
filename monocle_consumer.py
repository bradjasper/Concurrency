import monocle
from monocle import _o
monocle.init("tornado")

from monocle.stack import eventloop
from monocle.stack.network.http import HttpClient

@_o
def sleep():
    import time
    print "sleeping"
    yield 10
    time.sleep(1)
    print "done"
"""
def request():
    client = HttpClient()
    resp = yield client.request('http://google.com/')
    print resp.code, resp.body
"""

for x in xrange(100):
    monocle.launch(sleep())

eventloop.run()
