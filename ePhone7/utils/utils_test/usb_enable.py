import os

from ePhone7.utils.spud_serial import SpudSerial

ip_addr = SpudSerial.get_my_ip_addr()
actions = [
    {'cmd': 'cd /data/misc/adb', 'new_cwd': 'data/misc/adb', 'expect': ''},
    {'cmd': 'alias tftp="busybox tftp"', 'new_cwd': None, 'expect': ''},
    {'cmd': 'tftp -g -r adbkey.pub -l adb_keys %s' % ip_addr, 'new_cwd': None, 'expect': ''},
    {'cmd': 'chown system adb_keys', 'new_cwd': None, 'expect': ''},
    {'cmd': 'chmod 640 adb_keys', 'new_cwd': None, 'expect': ''},
    {'cmd': 'cd /data/property', 'new_cwd': 'data/property', 'expect': ''},
    {'cmd': 'echo -n mtp,adb > persist.sys.usb.config', 'new_cwd': None, 'expect': ''},
    {'cmd': 'reboot', 'new_cwd': '', 'expect': None, 'timeout': 10}
]
with open(os.path.join(os.getenv('HOME'), '.android', 'adbkey.pub')) as input_file:
    with open('/tftpboot/adbkey.pub', 'w') as output_file:
        key = input_file.read()
        output_file.write(key + '\n')
serial_dev = '/dev/ttyUSB0'
ss = SpudSerial(serial_dev)
for action in actions:
    (reply, after_prompt) = ss.do_action(action)
    print 'cmd: "%s", reply: "%s"' % (action['cmd'], reply)
    if after_prompt:
        print '  after_prompt: "%s"' % after_prompt
