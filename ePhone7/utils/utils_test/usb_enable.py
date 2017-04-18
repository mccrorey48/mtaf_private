import os

from ePhone7.utils.spud_serial import SpudSerial

ip_addr = SpudSerial.get_my_ip_addr()
actions = [
    {'cmd': 'cd /data/misc/adb', 'new_cwd': 'data/misc/adb'},
    {'cmd': 'alias tftp="busybox tftp"', 'new_cwd': None},
    {'cmd': 'tftp -g -r adbkey.pub -l adb_keys %s' % ip_addr, 'new_cwd': None},
    {'cmd': 'chown system adb_keys', 'new_cwd': None},
    {'cmd': 'chmod 640 adb_keys', 'new_cwd': None},
    {'cmd': 'cd /data/property', 'new_cwd': 'data/property'},
    {'cmd': 'echo -n mtp,adb > persist.sys.usb.config', 'new_cwd': None},
    {'cmd': 'reboot', 'new_cwd': '', 'timeout': 30}
]
with open(os.path.join(os.getenv('HOME'), '.android', 'adbkey.pub')) as input_file:
    with open('/tftpboot/adbkey.pub', 'w') as output_file:
        key = input_file.read()
        output_file.write(key + '\n')
serial_dev = '/dev/ttyUSB0'
ss = SpudSerial(serial_dev)
for action in actions:
    (reply, elapsed) = ss.do_action(action)
    lines = reply.split('\n')
    print 'cmd: %s\nelapsed: [%5.3f s]  \nreply: "%s"\n' % (action['cmd'], elapsed, lines[0])
    for line in lines[1:]:
        print ' '*7 + line
print 'readall: %s' % ss.readall()
