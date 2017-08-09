'use strict';

process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

var io = require('socket.io-client');
var http = require('http');

var socket;

var accessToken = "notARealKey";
var lastUpdate = 0;

function startWebsocket(accessToken) {
  socket = io.connect('https://aws.esiapi.io', {
    query: { auth: accessToken },
    path: '/drs/v2/socket.io/',
    reconnect: true,
    'reconnection limit': 3000,
    'max reconnection attempts': Infinity
  });

  var startup = true;
  socket.on('connect', function() {
    if (startup) {
      startup = false;
      console.log('socket connect');
    } else {
      console.log('socket connect (reconnection)');
    }

    var options = {
      type: 'corpCon',
      //type: 'presence',
      // type: 'callhistory',
      //type: 'google',
      lastUpdate: lastUpdate,
      accessToken: accessToken
    };

    socket.emit('join_room', options);
  });

  socket.on('callhistory-test2.test-eng.com-2202', function(data) {
    console.log('callhistory-test2.test-eng.com-2202', data);
  });

  socket.on('presence-test2.test-eng.com', function(data) {
    console.log('presence-test2.test-eng.com', data);
  });

  socket.on('corpCon-test2.test-eng.com', function(data) {
    console.log('corpCon-test2.test-eng.com', data);
  });

  socket.on('google-test2.test-eng.com-2202', function(data) {
    console.log('google-test2.test-eng.com-2202', data);
  });

  socket.on('disconnect', function() {
    console.log('socket disconnect');

    socket.io.opts.query = { auth: accessToken };
  });

  socket.on('error', function(err) {
    console.log('error', err);
  });
}

function go() {
  var options = {
    hostname: 'pro.esiapi.io',
    port: 80,
    path: '/aaa/v2/login',
    headers: {
      'Content-type': 'application/json'
    },
    method: 'POST',
  };

  function callback(res) {
    console.log('Status: ' + res.statusCode);
    console.log('Headers: ' + JSON.stringify(res.headers));
    res.setEncoding('utf8');
    res.on('data', function(body){
      console.log("body = " + body);
      var bodyObject = JSON.parse(body);
      var accessToken = bodyObject.accessToken;
      console.log("accessToken = " + accessToken);
      startWebsocket(accessToken);
    })

  }

  var req = http.request(options, callback);
  req.on('error', function(e){
    console.log(e)
  });
  req.write(JSON.stringify({username: "2202@test2.test-eng.com", password: "2202"}));
  req.end();
  //   .expect('Content-Type', /json/)
  //   .expect(function(res) {
  //     console.log(res)
  //   })
  // .expect(200, function);
  return "hello, y'all";
}

console.log(go());
