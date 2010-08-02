/*
 * The problem is right now this is all synchrnous. We should grab
 * all 150 items from Redis, then start all 150 HTTP Connections
 * then let them finish when they're ready.
 */

var sys = require('sys'),
    kiwi = require('kiwi'),
    http = require('http'),
    redis = kiwi.require('redis-client').createClient();

var chunk_size = 5;

function consume() {

    var messages = [];

    function _consume() {
        redis.lpop("redis_queue", function(err, reply) {
            if (err) {
                console.log("ERROR: " + err);
            } else if (!reply) {
                if (messages.length > 0) {
                    process_messages(messages);
                }
                setTimeout(consume, 500);
            } else {
                messages.push(JSON.parse(reply));
                console.log("MESSAGES: " + messages.length);

                if (messages.length >= chunk_size) {
                    process_messages(messages);
                    messages = [];
                }
            }
        });
        _consume();
    }
    _consume();
}
consume();

function process_messages(messages) {
    console.log("PROCESSING MESSAGES: " + messages.length);

    messages.forEach(function(message) {

        var client = http.createClient(80, message.download_url);
        var request = client.request('GET', '/', {'host': message.download_url});

        request.on('response', function (response) {

          response.setEncoding('utf8');

          response.on('data', function (chunk) {
           // console.log('BODY: ' + chunk.length);
          });

          response.on('end', function () {
              redis.incr(message.test_name, function(err, val) {
                console.log("FINISHED: " + val);
                consume();
              });

          });

        });
        request.end();

    });
}


function download_url(download_url, test_name) {

    console.log("DOWNLOADING: " + download_url);
    var client = http.createClient(80, download_url);
    var request = client.request('GET', '/', {'host': download_url});

    request.on('response', function (response) {

      response.setEncoding('utf8');

      response.on('data', function (chunk) {
//       console.log('BODY: ' + chunk.length);
      });

      response.on('end', function () {
          redis.incr(test_name, function(err, val) {
            console.log("FINISHED: " + val);
          });

      });

    });
    request.end();
}
