import serial
from lib.user_exception import UserException as Ux
import socket
from time import time


class SpudSerial:

    def __init__(self, serial_device):
        try:
            # current user has to belong to "dialout" group or be superuser
            # to open the serial port
            self.connection = serial.Serial(serial_device, 115200, timeout=1.0)
        except serial.serialutil.SerialException:
            raise Ux('serial port %s not available' % serial_device)
        self.do_action({'cmd': 'cd', 'new_cwd': 'data', 'expect': ''})

    def get_prompt(self):
        return 'root@r2d2:/' + self.cwd + ' # '

    @classmethod
    def get_my_ip_addr(cls):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_addr = s.getsockname()[0]
        s.close()
        return ip_addr

    def readall(self, timeout):
        buf = ''
        start_time = None
        while True:
            c = self.connection.read()
            if not len(c):
                if start_time is None:
                    start_time = time()
                elif time() - start_time > timeout:
                    return buf
            elif c != '\r':
                start_time = None
                buf += c

    def send_cmd(self, cmd, timeout):
        # truncate cmd at first linefeed (no multiline commands)
        # then add a linefeed to the result
        cmd = cmd.split('\n')[0] + '\n'
        self.connection.write(cmd)
        reply = self.readall(timeout)
        if not reply.startswith(cmd):
            raise Ux('reply "%s" does not start with "%s"' % (reply, cmd))
        if not reply.find(self.get_prompt()):
            raise Ux('reply "%s" does not contain "%s"' % (reply, self.get_prompt()))
        return reply[len(cmd):].split(self.get_prompt())

    def do_action(self, action):
        if action['new_cwd'] is not None:
            self.cwd = action['new_cwd']
        if 'timeout' in action:
            timeout = action['timeout']
        else:
            timeout = 2
        (reply, after_prompt) = self.send_cmd(action['cmd'], timeout)
        if action['expect'] is not None and reply != action['expect']:
            raise Ux('expected reply <%s>, got <%s>' % (action['expect'], reply))
        return (reply, after_prompt)


