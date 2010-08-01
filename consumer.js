/*
 * The problem is right now this is all synchrnous. We should grab
 * all 150 items from Redis, then start all 150 HTTP Connections
 * then let them finish when they're ready.
 */

var sys = require('sys'),
    kiwi = require('kiwi'),
    http = require('http'),
    redis = kiwi.require('redis-client').createClient();

function consume() {
    redis.blpop("redis_queue", 0, function(err, reply) {
        if (err) {
            console.log("ERROR: " + err);
            return;
        }

        data = JSON.parse(reply[1]);

        console.log("reply " + reply);
        download_url(data.download_url, data.test_name, consume);

    });
}

consume();

function download_url(download_url, test_name, callback) {

    var client = http.createClient(80, download_url);
    var request = client.request('GET', '/', {'host': download_url});
    request.end();

    request.on('response', function (response) {

      response.setEncoding('utf8');

      response.on('data', function (chunk) {
 //       console.log('BODY: ' + chunk.length);
      });

      response.on('end', function () {
          redis.incr(test_name, function(err, val) {
//            console.log("FINISHED: " + val);
          });

      });

    });
    callback();
}
