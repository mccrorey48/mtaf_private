'use strict';

process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

var io = require('socket.io-client');

var socket;

var lastUpdate = 0;

function startWebsocket(accessToken) {
  socket = io.connect('http://aws.esiapi.io', {
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
    log.warn('callhistory-test2.test-eng.com-2202', data);
  });

  socket.on('presence-test2.test-eng.com', function(data) {
    log.warn('presence-test2.test-eng.com', data);
  });

  socket.on('corpCon-test2.test-eng.com', function(data) {
    log.warn('corpCon-test2.test-eng.com', data);
  });

  socket.on('google-test2.test-eng.com-2202', function(data) {
    log.warn('google-test2.test-eng.com-2202', data);
  });

  socket.on('disconnect', function() {
    log.warn('socket disconnect');

    socket.io.opts.query = { auth: accessToken };
  });

  socket.on('error', function(err) {
    log.warn('error', err);
  });
}

startWebsocket(vars.get("selectAccessToken"));
