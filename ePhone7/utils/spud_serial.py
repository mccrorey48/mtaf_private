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
        self.cwd = None
        self.do_action({'cmd': 'cd', 'new_cwd': 'data'})

    def get_prompt(self):
        return 'root@r2d2:/' + self.cwd + ' # '

    @classmethod
    def get_my_ip_addr(cls):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_addr = s.getsockname()[0]
        s.close()
        return ip_addr

    def readall(self, timeout=1):
        """
            read the serial port one character at a time, until subsequent calls do
            not return a character for "timeout" seconds
        """
        reply = ''
        start_time = None
        while True:
            c = self.connection.read()
            if not len(c):
                if start_time is None:
                    start_time = time()
                elif time() - start_time > timeout:
                    return reply
            elif c != '\r':
                start_time = None
                reply += c

    def expect(self, cmd, expect_text, timeout=1):
        """
            truncate cmd at first linefeed (no multiline commands) then add '\n';
            write the '\n'-terminated cmd to the serial port (cmd can be empty string);
            read the serial port one character at a time and add to 'reply' string,
            until 'reply' ends with expect_text;
            expect the reply to start with the echo of the command, and remove it;
            if no expect_text received after 'timeout' seconds, raise an exception;
            if expect_text is received, return 'reply.
        """
        reply = ''
        cmd = cmd.split('\n')[0] + '\n'
        self.connection.write(cmd)
        start_time = time()
        while True:
            c = self.connection.read()
            if c != '\r':
                reply += c
            elapsed = time() - start_time
            if reply.endswith(expect_text):
                if not reply.startswith(cmd):
                    raise Ux('reply "%s" does not start with "%s"' % (reply, cmd))
                return reply[len(cmd):], elapsed
            if time() - start_time > timeout:
                raise Ux("expect: %s second timeout exceeded waiting for %s" % (timeout, expect_text))

    def do_action(self, action):
        if 'new_cwd' in action and action['new_cwd'] is not None:
            self.cwd = action['new_cwd']
        if 'timeout' in action:
            timeout = action['timeout']
        else:
            timeout = 1
        if 'expect' in action and len(action['expect']):
            reply, elapsed = self.expect(action['cmd'], action['expect'], timeout)
            return reply, elapsed
        else:
            reply, elapsed = self.expect(action['cmd'], self.get_prompt(), timeout)
            return reply[:-1 * len(self.get_prompt())], elapsed
