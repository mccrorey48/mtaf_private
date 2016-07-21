import lib.softphone.pjsua_lib as pjl
from lib.common.user_exception import UserException as Ux
import Queue
import lib.common.logging_esi as logging_esi
from lib.common.wrappers import Trace
from time import time, sleep
from lib.softphone.wav_audio import create_wav_file
from lib.common.configure import cfg
import re
import random

log = logging_esi.get_logger('esi.softphone')
softphones = {}


class Softphone:

    account = None
    uri = None
    status = None

    @Trace(log)
    def __init__(self, user_name, null_snd, tcp):
        user_cfg = cfg.site['Accounts'][user_name]
        pbfile = user_cfg['pbfile']
        create_wav_file(pbfile)
        uri = 'sip:%s@%s' % (user_cfg['UserId'], user_cfg['DomainName'])
        proxy = user_cfg['Proxy']
        passwd = user_cfg['Password']
        if len(softphones) == 0:
            pjl.lib.start(null_snd=null_snd, dns_list=user_cfg['dns_list'], tcp=tcp)
            pjl.cmd_q = Queue.Queue()
            pjl.lib.connect_monitor(None)
            pjl.wav_dir = 'wav/'
        self.uri = uri
        pjl.pbfile_strings[self.uri] = pbfile
        self.account = pjl.lib.add_account(self.uri, proxy, passwd)
        softphones[user_name] = self

    @Trace(log)
    def wait_for_call_status(self, desired_status, timeout):
        start = time()
        while time() - start < timeout:
            if not pjl.cmd_q.empty():
                txt = pjl.cmd_q.get()
                log.debug("[wait_for_call_status] cmd_q: " + txt)
                m = re.match('call\s+(\S+)\s.*(sip:\d+@\S+).*(sip:\d+@\S+)', txt)
                if m:
                    self.status = m.group(1)
                    src_uri = m.group(2)
                    log.debug("[wait_for_call_status] %s status = %s" % (src_uri, self.status))
                    if self.status == desired_status and src_uri == self.uri:
                        log.debug("[wait_for_call_status] %s successfully reached status %s" % (self.uri, self.status))
                        # return how long the wait was, in case the caller wants to check
                        return time() - start
                    if self.status == 'call' and desired_status == 'early':
                        self.teardown_call()
                        raise Ux('wait for call status "early" terminated call because status was "call"')
                sleep(0.1)
        else:
            raise Ux('wait for call status "%s" timed out after %s seconds' % (desired_status, timeout))

    # using two soft phone accounts, have one call the other
    # then wait for the call status to verify both calls are set up
    @Trace(log)
    def make_call(self, _dst_uri):
        if self.account.info().reg_status != 200:
            raise Ux("Can't set up call, registration status (src) %s" % self.account.info().reg_status)
        log.debug("Calling %s" % _dst_uri)
        pjl.current_calls[self.uri] = self.account.make_call(_dst_uri, pjl.MyCallCallback())

    @Trace(log)
    def leave_msg(self, length=None):
        if self.uri not in pjl.current_calls:
            raise Ux("%s not in current_calls" % self.uri)
        sleep(10)
        pjl.current_calls[self.uri].dial_dtmf('2')
        if length is None:
            random.seed(time())
            length = random.randrange(10, 30, 1)
        sleep(length)

    @Trace(log)
    def teardown_call(self):
        if self.uri in pjl.current_calls:
            call = pjl.current_calls[self.uri]
            # print "STATE = %d" % call.info().state
            call.hangup()
            log.debug("%s hanging up" % self.uri)
            log.debug("calling wait_for_call_status(%s, 'end', 15)" % self.uri)
            self.wait_for_call_status('disconnected', 15)

    @Trace(log)
    def dial_dtmf(self, dtmf_string):
        if self.uri in pjl.current_calls:
            for c in list(dtmf_string):
                log.debug('%s:send dtmf %s' % (self.uri, c))
                pjl.current_calls[self.uri].dial_dtmf(c)
                sleep(0.3)

    @Trace(log)
    def set_monitor_on(self):
        pjl.lib.connect_monitor(self.uri)

    @Trace(log)
    def set_monitor_off(self):
        pjl.lib.connect_monitor(None)


def get_softphone(user_name='Auto TesterC', null_snd=False, tcp=False):
    if user_name in softphones:
        return softphones[user_name]
    else:
        return Softphone(user_name, null_snd, tcp)

