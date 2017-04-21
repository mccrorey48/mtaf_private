from pyand import ADB, Fastboot

from ePhone7.utils.spud_serial import SpudSerial

actions = [
    {'cmd': 'reboot\n', 'new_cwd': '', 'expect': 'Hit any key to stop autoboot:', 'timeout': 30},
    {'cmd': '\n', 'expect': '=> ', 'timeout': 5},
    {'cmd': 'mmc dev 2\n', 'expect': 'mmc2(part 0) is current device\n=> '},
    {'cmd': 'mmc setdsr 2\n', 'expect': 'set dsr OK, force rescan\n=> '},
    {'cmd': 'fastboot\n', 'expect': '0x4\nUSB_RESET\nUSB_PORT_CHANGE 0x4\n'}
]

serial_dev = '/dev/ttyUSB0'

ss = SpudSerial(serial_dev)
for action in actions:
    (reply, elapsed) = ss.do_action(action)
    print '[%5.3fs] cmd %s, expect %s, received %d chars' % (elapsed, repr(action['cmd']), repr(action['expect']), len(reply))
    ss.connection.reset_input_buffer()

fb = Fastboot()
# print '>>> fastboot devices: %s' % fb.get_devices()
fb_cmds = [
    "flash boot ePhone7/aosps/2.1.3/boot.img",
    "flash system ePhone7/aosps/2.1.3/system.img",
    "flash recovery ePhone7/aosps/2.1.3/recovery.img",
    "reboot"
    ]
for cmd in fb_cmds:
    print ">>> fastboot " + cmd
    print fb.run_cmd(cmd)
adb = ADB()
adb.run_cmd("install -r ePhone7/apks/10_0_9.apk")
action = {'cmd': 'reboot\n', 'new_cwd': '', 'timeout': 30}
(reply, elapsed) = ss.do_action(action)
print '[%5.3fs] cmd %s, expect %s, received %d chars' % (elapsed, repr(action['cmd']), repr(action['expect']), len(reply))
