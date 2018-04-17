#!/bin/bash
/usr/local/bin/node $APPIUM_HOME/build/lib/main.js --address "127.0.0.1" --debug-log-spacing --log "/tmp/appium2.log" --log-timestamp --log-level "debug" --local-timezone --session-override

