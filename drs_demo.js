'use strict';

process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

var io = require('socket.io-client');
var http = require('http');

var socket;

var accessToken = "notARealKey";
var lastUpdate = 0;

function startWebsocket(accessToken) {
  //socket = io.connect('http://aws.esiapi.io', {
  socket = io.connect('http://10.3.1.5', {
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

  socket.on('callhistory-SVAutoCustomer-1000', function(data) {
    console.log('callhistory-SVAutoCustomer-1000', data);
  });

  socket.on('presence-SVAutoCustomer', function(data) {
    console.log('presence-SVAutoCustomer', data);
  });

  socket.on('corpCon-SVAutoCustomer', function(data) {
    console.log('corpCon-SVAutoCustomer', data);
  });

  socket.on('google-SVAutoCustomer-1000', function(data) {
    console.log('google-SVAutoCustomer-1000', data);
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
    hostname: '10.3.1.5',
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
  req.write(JSON.stringify({username: "1000@SVAutoCustomer", password: "1000"}));
  req.end();
  //   .expect('Content-Type', /json/)
  //   .expect(function(res) {
  //     console.log(res)
  //   })
  // .expect(200, function);
  return "hello, y'all";
}

console.log(go());
