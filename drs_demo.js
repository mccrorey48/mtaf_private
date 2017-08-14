'use strict';

process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

var io = require('socket.io-client');
var http = require('http');

var socket;

var api_url = 'http://aws.esiapi.io';
var drs_path = '/drs/v2/socket.io';
var aaa_path = '/aaa/v2/login';
var lastUpdate = 0;
var users = [
  { name: "2202", domain:"test2.test-eng.com", password: "2202"},
  { name: "2203", domain:"test2.test-eng.com", password: "2202"},
  { name: "2204", domain:"test2.test-eng.com", password: "2202"},
  { name: "2205", domain:"test2.test-eng.com", password: "2202"}
  ];

function startWebsocket(accessToken, user) {
  socket = io.connect(api_url, {
    query: { auth: accessToken },
    path: drs_path,
    reconnect: true,
    'reconnection limit': 3000,
    'max reconnection attempts': Infinity
  });

  var startup = true;
  var user_id_text = user.domain + '-' + user.name;
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

  socket.on('callhistory-' + user_id_text, function(data) {
    console.log('callhistory-'+ user_id_text, data);
  });

  socket.on('presence-' + user.domain, function(data) {
    console.log('presence-' + user.domain, data);
  });

  socket.on('corpCon-' + user.domain, function(data) {
    console.log('corpCon-' + user.domain, data);
  });

  socket.on('google-' + user_id_text, function(data) {
    console.log('google-' + user_id_text, data);
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
    hostname: api_url,
    port: 80,
    path: aaa_path,
    headers: {
      'Content-type': 'application/json'
    },
    method: 'POST',
  };

  function get_callback(user) {
    return function(res){
      console.log('Status: ' + res.statusCode);
      console.log('Headers: ' + JSON.stringify(res.headers));
      res.setEncoding('utf8');
      res.on('data', function(body){
        console.log("body = " + body);
        var bodyObject = JSON.parse(body);
        var accessToken = bodyObject.accessToken;
        console.log("accessToken = " + accessToken);
        startWebsocket(accessToken, user);
      })
    }
  }

  users.forEach(function(user){
    var req = http.request(options, get_callback(user));
    req.on('error', function(e){
      console.log(e)
    });
    req.write(JSON.stringify({username: user.name + '@' + user.domain, password: user.password}));
    req.end(0);
  });
}

go();
console.log("started a websocket");
