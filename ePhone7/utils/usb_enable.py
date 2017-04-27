import os
from ePhone7.utils.spud_serial import SpudSerial
import lib.logging_esi as logging
log = logging.get_logger('esi.usb_enable')


def usb_enable():
    ip_addr = SpudSerial.get_my_ip_addr()
    actions = [
        {'cmd': 'cd /data/misc/adb\n', 'new_cwd': 'data/misc/adb'},
        {'cmd': 'alias tftp="busybox tftp"\n', 'new_cwd': None},
        {'cmd': 'tftp -g -r adbkey.pub -l adb_keys %s\n' % ip_addr, 'new_cwd': None},
        {'cmd': 'chown system adb_keys\n', 'new_cwd': None},
        {'cmd': 'chmod 640 adb_keys\n', 'new_cwd': None},
        {'cmd': 'cd /data/property\n', 'new_cwd': 'data/property'},
        {'cmd': 'echo -n mtp,adb > persist.sys.usb.config\n', 'new_cwd': None},
        {'cmd': 'reboot\n', 'new_cwd': '', 'timeout': 30}
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
        log.debug('cmd: %s\nelapsed: [%5.3f s]  \nreply: "%s"\n' % (action['cmd'], elapsed, lines[0].encode('string_escape')))
        for line in lines[1:]:
            log.debug(' '*7 + line.encode('string_escape'))
    flushed = ss.flush()[0]
    for line in flushed.split('\n'):
        log.debug('flushed: %s' % line.encode('string_escape'))
