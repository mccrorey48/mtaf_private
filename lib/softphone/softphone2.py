# softphone class that uses simple_pj
import random
import re
from time import time, sleep

import lib.logging_esi as logging_esi
from lib.wrappers import Trace

import lib.softphone.simple_pj as pj
from lib.softphone.wav_audio import create_wav_file
from lib.user_exception import UserException as Ux, UserTimeoutException as Tx

log = logging_esi.get_logger('esi.softphone2')


class Softphone:

    lib = None
    pbfile = None
    dst_uri = None
    rec_id = None
    rec_slot = None

    @Trace(log)
    def __init__(self, uri, proxy, password, null_snd=True, dns_list=None, tcp=False,
                 pbfile=None, rec=True, quiet=True):
        self.uri = uri
        self.pbfile = pbfile
        if not self.lib:
            Softphone.lib = pj.PjsuaLib()
            self.lib.start(null_snd=null_snd, dns_list=dns_list, tcp=tcp)
        if self.pbfile:
            create_wav_file(self.pbfile, quiet)
        m = re.match('sip:([^@]+)@(.+)', self.uri)
        if m:
            self.lib.add_account(m.group(1), m.group(2), proxy, password)
            self.account_info = pj.account_infos[self.uri]

    @Trace(log)
    def wait_for_call_status(self, desired_status, timeout=30):
        # possible desired_status values: 'call', 'idle', 'early', 'hold'
        start = time()
        while time() - start < timeout:
            if self.account_info.call_status == desired_status:
                return time() - start
            sleep(0.1)
            if self.account_info.call_status == 'call' and desired_status == 'early':
                self.teardown_call()
                raise Ux('wait for call status "early" terminated call because status was "call"')
        else:
            raise Tx('wait for call status "%s" timed out after %s seconds' % (desired_status, timeout))

    @Trace(log)
    def make_call(self, dst_uri):
        self.dst_uri = dst_uri
        if self.account_info.reg_status != 200:
            raise Ux("Can't set up call, registration status (src) %s" % self.account_info.reg_status)
        log.debug("%s calling %s" % (self.uri, self.dst_uri))
        # print self.dst_uri
        self.account_info.call = self.account_info.account.make_call_to_softphone(self.dst_uri)
        self.account_info.call.set_callback(pj.MyCallCallback(self.account_info))

    @Trace(log)
    def end_call(self):
        if not self.account_info.call:
            raise Ux("end_call(): %s not in call" % self.uri)
        log.debug("%s ending call to %s" % (self.uri, self.dst_uri))
        self.account_info.call.hangup()

    @Trace(log)
    def leave_msg(self, length=None):
        if not self.account_info.call:
            raise Ux("leave_msg(): %s not in call" % self.uri)
        sleep(10)
        self.account_info.call.dial_dtmf('2')
        if length is None:
            random.seed(time())
            length = random.randrange(10, 30, 1)
        sleep(length)

    def teardown_call(self):
        if self.account_info.call:
            self.account_info.call.hangup()
            log.debug("%s hanging up" % self.uri)
            log.debug("calling wait_for_call_status(%s, 'end', 15)" % self.uri)
            self.wait_for_call_status('disconnected', 15)

    @Trace(log)
    def dial_dtmf(self, dtmf_string):
        if self.account_info.call:
            for c in list(dtmf_string):
                log.debug('%s:send dtmf %s' % (self.uri, c))
                self.account_info.call.dial_dtmf(c)
                sleep(0.3)

    @Trace(log)
    def set_monitor_on(self):
        pass

    @Trace(log)
    def set_monitor_off(self):
        pass

    @Trace(log)
    def connect_media(self):
        if self.rec_id is None:
            raise Ux("connect_media: no media exists")
        self.rec_slot = self.lib.recorder_get_slot(self.rec_id)
        my_uri = self.call.info().account.info().uri
        # self.media_call_slot is set to the call's conference slot when connecting media,
        # and set to None when disconnecting, so if it is not None, this is a reconnect
        if self.media_call_slot is not None:
            # if self.media_call_slot is not None but is not the current call's conference slot,
            # it isn't a reconnect, it's a structural program error
            if self.media_call_slot != self.call.info().conf_slot:
                raise Ux("connect_media: call at slot %d media already connected to call slot %d"
                         % (self.call.info().conf_slot, self.media_call_slot))
            log.debug("%s: disconnecting call slot %d from recorder %s at slot %d"
                      % (my_uri, self.media_call_slot, self.rec_id, self.rec_slot))
            lib.conf_disconnect(self.media_call_slot, self.rec_slot)
            if self.player_id is not None:
                self.pb_slot = lib.player_get_slot(self.player_id)
                log.debug("%s: disconnecting player %s at slot %d to call slot %d"
                          % (my_uri, self.player_id, self.pb_slot, self.media_call_slot))
                lib.conf_disconnect(self.pb_slot, self.media_call_slot)
            self.media_call_slot = None
        log.debug("%s: connecting call slot %d to recorder %s at slot %d"
                  % (my_uri, self.call.info().conf_slot, self.rec_id, self.rec_slot))
        lib.conf_connect(self.call.info().conf_slot, self.rec_slot)
        # if there is a player ID then the player was created during create_media and we can connect it, too
        if self.player_id is not None:
            self.pb_slot = lib.player_get_slot(self.player_id)
            log.debug("%s: connecting player %s at slot %d to call slot %d"
                      % (my_uri, self.player_id, self.pb_slot, self.call.info().conf_slot))
            lib.conf_connect(self.pb_slot, self.call.info().conf_slot)
        self.media_call_slot = self.call.info().conf_slot
