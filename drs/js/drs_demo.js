'use strict';

process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

var io = require('socket.io-client');
var http = require('http');
var fs = require('fs');
var util = require('util');
var csv = require('fast-csv');
var sprintf = require('sprintf');


var drs_path = '/drs/v2/socket.io';
var aaa_path = '/aaa/v2/login';
var lastUpdate = 0;
var api_url;
var lab = false;
var start = Date.now();

// test configuration values
var option_types = ['corpCon', 'callhistory', 'google'];
// var option_types = ['corpCon'];
var user_count = 0;
var max_user_count = 100;

var users;
var csv_file;
if (lab) {
  api_url = '10.3.1.5';
  csv_file = 'drs/csv/lab_users_concurrent.csv';
} else {
  api_url = 'dev.esiapi.io';
  csv_file = 'drs/csv/pro_users_concurrent.csv';
}

csv
.fromPath(csv_file, {headers: ["name", "domain", "username", "password"]})
.on("data", function(user){
  if (user.name !== "name" && user_count < max_user_count) {
    user_count += 1;
    go(user);
  }
});

var log_file = fs.createWriteStream('log/drs_test.log', {flags : 'w'});
var blf_log_file = fs.createWriteStream('log/blf_updates.log', {flags : 'w'});
var log_stdout = process.stdout;

function log_blf(s) {
  var d = new Date();
  var timestamp = sprintf("%02d:%02d:%02d.%03d", d.getHours(), d.getMinutes(), d.getSeconds(), d.getMilliseconds());
  blf_log_file.write(sprintf("%s: %s\n", timestamp, s))
}

function log(s) {
  var elapsed = Date.now() - start;
  var msg = util.format('%sms: %s\n', elapsed, s) ;
  log_file.write(msg);
  log_stdout.write(msg);
}

function startWebsocket(accessToken, user, option_type) {
  var socket;
  var last_blf = null;
  log("starting " + option_type + " websocket for user " + user.name + "@" + user.domain);
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
      log(option_type + ' socket connect');
    } else {
      log(option_type + ' socket connect (reconnection)');
    }

    var options = {
      type: option_type,
      lastUpdate: lastUpdate,
      accessToken: accessToken
    };

    socket.emit('join_room', options);
  });

  socket.on('callhistory-' + user.domain + '-' + user.name, function(data) {
    log('[' + user.name + ']["callhistory-'+ user.domain + '",'  + JSON.stringify(data));
  });

  socket.on('presence-' + user.domain, function(data) {
    log('[' + user.name + ']["presence-'+ user.domain + '",'  + JSON.stringify(data));
  });

  socket.on('corpCon-' + user.domain, function(data) {
    log('[' + user.name + ']["corpCon-'+ user.domain + '",'  + JSON.stringify(data));
    if (data.blf !== last_blf) {
      log_blf('[' + user.name + '] ' + data.blf);
      last_blf = data.blf
    }
  });

  socket.on('google-' + user.domain + '-' + user.name, function(data) {
    log('google-' + user.domain + '-' + user.name + JSON.stringify(data));
  });

  socket.on('disconnect', function() {
    log('socket disconnect');

    socket.io.opts.query = { auth: accessToken };
  });

  socket.on('error', function(err) {
    log('error', err);
  });

  // socket.on('connect_timeout', function(err) {
  //   log('connect timeout', err);
  // });
}

function go(user) {
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
      log('Status: ' + res.statusCode);
      log('Headers: ' + JSON.stringify(res.headers));
      res.setEncoding('utf8');
      res.on('data', function(body){
        log("body = " + body);
        var bodyObject = JSON.parse(body);
        var accessToken = bodyObject.accessToken;
        log("accessToken = " + accessToken);
        option_types.forEach(function(option_type) {
          startWebsocket(accessToken, user, option_type);
        });
      })
    }
  }

  // var req = http.request(options, get_callback(user));
  // req.on('error', function(e){
  //   log(e)
  // });
  // req.write(JSON.stringify({username: "2202@test2.test-eng.com", password: "2202"}));
  // req.end();
  // users.forEach(function(user){
  var req = http.request(options, get_callback(user));
  req.on('error', function(e){
    log(e)
  });
  req.write(JSON.stringify({username: user.name + '@' + user.domain, password: user.password}));
  req.end(0);
  // });
}


