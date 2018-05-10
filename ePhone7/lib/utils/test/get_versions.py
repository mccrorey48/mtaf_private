from ePhone7.lib.utils.spud_serial import SpudSerial
from ePhone7.config.configure import cfg
import re
from mtaf.ADB import ADB
import six

re_aosp = re.compile('\[ro\.build\.id\]:\s+\[(.*)\]')
action = {'cmd': 'getprop\n', 'timeout': 10}

ss = SpudSerial(cfg.site['SerialDev'])
(reply, elapsed, groups) = ss.do_action(action)
for line in reply.split('\n'):
    if re_aosp.match(line):
        six.print_("AOSP version: " + re_aosp.match(line).group(1))
adb = ADB()
output = adb.run_cmd('shell dumpsys package com.esi_estech.ditto')
six.print_('APK Version: ' + re.match('(?ms).*Packages:.*?versionName=(\d+\.\d+\.\d+)', output).group(1))
