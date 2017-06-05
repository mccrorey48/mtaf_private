import serial
from lib.user_exception import UserException as Ux
import socket
from time import time, sleep
from contextlib import contextmanager
import lib.logging_esi as logging_esi
from lib.wrappers import Trace
import re

log = logging_esi.get_logger('esi.spud_serial')


class SpudSerial:

    def __init__(self, serial_device, pwd_check=True):
        try:
            # current user has to belong to "dialout" group or be superuser
            # to open the serial port
            self.connection = serial.Serial(serial_device, 115200, timeout=1.0)
        except serial.serialutil.SerialException:
            raise Ux('serial port %s not available' % serial_device)
        self.cwd = None
        if pwd_check:
            self.do_action({'cmd': 'cd\n', 'new_cwd': 'data'})

    def get_prompt(self):
        return 'root@r2d2:/' + self.cwd + ' # '

    @contextmanager
    def with_timeout(self, timeout):
        old_timeout = self.connection.timeout
        log.debug("changing timeout from %.3f to %.3f" % (old_timeout, timeout))
        self.connection.timeout = timeout
        yield
        log.debug("changing timeout from %.3f to %.3f" % (self.connection.timeout, old_timeout))
        self.connection.timeout = old_timeout

    @classmethod
    def get_my_ip_addr(cls):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_addr = s.getsockname()[0]
        s.close()
        return ip_addr

    @Trace(log)
    def expect(self, cmd, expect_text, timeout=5):
        """
            write 'cmd' to the serial port;
            read the serial port one character at a time and add to 'reply' string, skipping '\r' characters, 
                until 'reply' ends with 'expect_text';
            if no expect_text received after 'timeout' seconds, raise an exception;
            if expect_text is received, return 'reply'.
        """
        log.debug('cmd "%s", expect_text "%s"' % (repr(cmd), repr(expect_text)))
        expect_text = '\('.join(expect_text.split('('))
        expect_text = '\)'.join(expect_text.split(')'))
        expect_re = re.compile('(?ms).*(' + expect_text + ')')
        reply = ''
        log_str = ''
        if len(cmd):
            self.connection.write(cmd)
        start_time = time()
        while True:
            try:
                c = self.connection.read()
            except serial.SerialException as e:
                log.debug("ignoring SerialException: %s" % e)
                c = ''
                sleep(1)
            if len(c) and c != '\r' and ord(c) < 0xff:
                reply += c
                if c == '\n':
                    # log.debug('>>' + log_str.encode('string_escape'))
                    log_str = ''
                else:
                    log_str += c
            elapsed = time() - start_time
            match = expect_re.match(reply)
            if match:
                return reply, elapsed, match
            if time() - start_time > timeout:
                raise Ux("expect: %s second timeout exceeded waiting for %s; reply = '%s'" % (timeout, expect_text, reply.encode('string_escape')))

    @Trace(log)
    def flush(self, timeout=5):
        """
            read the serial port one character at a time and add to 'reply' string, skipping '\r' characters, 
                until no characters have been received for 'timeout' seconds;
            return 'reply'.
        """
        start_time = time()
        with self.with_timeout(timeout):
            reply = ''
            while True:
                c = self.connection.read(timeout)
                if len(c) == 0:
                    return reply, time() - start_time
                if c != '\r':
                    reply += c

    @Trace(log)
    def do_action(self, action):
        """
            wrapper for calling "expect"
            - populates the "cmd", "expect_text" and "timeout" arguments from "action" attributes
            - if "expect" attribute is None or is missing or has length 0, sets the "expect_text"
              argument to the current prompt string (which gets dynamically modified by the "new_cwd" attribute)
        """
        if 'new_cwd' in action and action['new_cwd'] is not None:
            self.cwd = action['new_cwd']
        if 'timeout' in action:
            timeout = action['timeout']
        else:
            timeout = 1
        if 'expect' not in action or action['expect'] is None or len(action['expect']) == 0:
            expected = self.get_prompt()
        else:
            expected = action['expect']
        try:
            reply, elapsed, match = self.expect(action['cmd'], expected, timeout)
        except Ux as e:
            flushed = self.flush()[0]
            for line in flushed.split('\n'):
                log.debug('flushed: %s' % line.encode('string_escape'))
            raise e
        else:
            # for line in reply.split('\n'):
            #     log.debug(line.encode('string_escape'))
            log.debug('expect matched "%s" in %5.3f seconds' % (match.groups(), elapsed))
            return reply, elapsed, match.groups()
