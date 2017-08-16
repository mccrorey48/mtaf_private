'use strict';

process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

var io = require('socket.io-client');
var http = require('http');


var drs_path = '/drs/v2/socket.io';
var aaa_path = '/aaa/v2/login';
var lastUpdate = 0;
var users;
var api_url;
var lab = false;
var option_type = 'corpCon';
// var option_type = 'presence';
// var option_type = 'callhistory';
// var option_type = 'google';

if (lab) {
  api_url = '10.3.1.5';
  users = [
    { name: "1000", domain:"SVAutoCustomer", password: "1000"},
    { name: "1001", domain:"SVAutoCustomer", password: "1001"},
    { name: "1002", domain:"SVAutoCustomer", password: "1002"},
    { name: "1003", domain:"SVAutoCustomer", password: "1003"}
  ];
} else {
  api_url = 'pro.esiapi.io';
  users = [
    { name: "2202", domain:"test2.test-eng.com", password: "2202"},
    { name: "2203", domain:"test2.test-eng.com", password: "2203"},
    { name: "2204", domain:"test2.test-eng.com", password: "2204"},
    { name: "2205", domain:"test2.test-eng.com", password: "2205"}
  ];
}

function startWebsocket(accessToken, user) {
  var socket;
  console.log("starting websocket for user " + user.name + '@' + user.domain);
  socket = io.connect('http://' + api_url, {
    query: { auth: accessToken },
    path: drs_path,
    reconnect: true,
    'reconnection limit': 3000,
    // 'timeout': 2000,
    transports: ['websocket'],
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
      type: option_type,
      lastUpdate: lastUpdate,
      accessToken: accessToken
    };

    socket.emit('join_room', options);
  });

  socket.on('callhistory-' + user.domain + '-' + user.name, function(data) {
    console.log('callhistory-'+ user.domain + '-' + user.name, data);
  });

  socket.on('presence-' + user.domain, function(data) {
    console.log('presence-' + user.domain, data);
  });

  socket.on('corpCon-' + user.domain, function(data) {
    console.log('corpCon-' + user.domain + '-' + user.name, data);
  });

  socket.on('google-' + user.domain + '-' + user.name, function(data) {
    console.log('google-' + user.domain + '-' + user.name, data);
  });

  socket.on('disconnect', function() {
    console.log('socket disconnect');

    socket.io.opts.query = { auth: accessToken };
  });

  socket.on('error', function(err) {
    console.log('error', err);
  });

  // socket.on('connect_timeout', function(err) {
  //   console.log('connect timeout', err);
  // });
}

function go() {
  var options = {
    hostname: api_url,
    port: 80,
    path: '/aaa/v2/login',
    // path: aaa_path,
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

  // var req = http.request(options, get_callback(user));
  // req.on('error', function(e){
  //   console.log(e)
  // });
  // req.write(JSON.stringify({username: "2202@test2.test-eng.com", password: "2202"}));
  // req.end();
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

