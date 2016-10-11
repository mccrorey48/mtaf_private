import re
import struct
import threading
from os import rename, getcwd, remove
from time import sleep

import lib.logging_esi as logging
import pjsua as pj
from lib.wrappers import Trace

from lib.user_exception import UserException as Ux

PjsuaError = pj.Error
wav_dir = 'wav/'
current_calls = {}
cmd_q = None

log = logging.get_logger('esi.pjsua_lib')
log.spaces = 0
recorder_call_cbs = {}
pbfile_strings = {}
monitor_uri = None


media_state_text = {
    0: 'NULL',
    1: 'ACTIVE',
    2: 'LOCAL HOLD',
    3: 'REMOTE HOLD',
    4: 'ERROR'
}

call_state_text = {
    0: 'null',
    1: 'calling',
    2: 'incoming',
    3: 'early',
    4: 'connecting',
    5: 'confirmed',
    6: 'disconnected'
}


# callback used by the pjsip/pjsua libraries for logging
def pjl_log_cb(level, _str, _len):
    sip_match = re.match('.*(Request|Response)', _str)
    lines = ["log_cb(%d): %s" % (level, line) for line in _str.splitlines()]
    if level == 1:
        for line in lines:
            log.warn(line)
    elif level == 2:
        for line in lines:
            log.info(line)
    elif sip_match:
        log.trace(lines[0])
        for line in lines:
            log.debug(line)
    else:
        for line in lines:
            log.debug(line)


@Trace(log)
def pj_err_decode(e):
    return "Exception: %s %s %s" % (e.err_code, e.op_name, e._err_msg)


class MyAccountCallback(pj.AccountCallback):
    """Callback to handle account setup and incoming calls"""
    sem = None

    @Trace(log)
    def __init__(self):
        pj.AccountCallback.__init__(self)

    @Trace(log)
    def wait(self):
        self.sem = threading.Semaphore(0)
        self.sem.acquire()

    @Trace(log)
    def on_reg_state(self):
        log.debug("%s:  on_reg_state callback - registration status = %s" % (self.account.info().uri, self.account.info().reg_status))
        if self.sem and self.account.info().reg_status >= 200:
            log.debug("releasing wait semaphore")
            self.sem.release()

    @Trace(log)
    def on_incoming_call(self, call):
        # global current_calls
        my_uri = call.info().uri[1:-1]
        if my_uri in current_calls:
            call.answer(486, "Busy")
            return
        log.debug("%s: incoming call from %s" % (my_uri, call.info().remote_uri))
        current_calls[my_uri] = call
        call.set_callback(MyCallCallback(call))
        call.answer(200)


class MyCallCallback(pj.CallCallback):
    """Callback to receive events from Call"""
    @Trace(log)
    def __init__(self, call=None):
        pj.CallCallback.__init__(self, call)
        self.media_call_slot = None
        self.rec_slot = None
        self.rec_id = None
        self.player_id = None
        self.pb_slot = None
        self.old_pbfile = None
        self.call_state = 'idle'
        self.media_connected = False

    # when creating and destroying media, the player is optional (depending on if pbfile is defined)
    # so the logical condition of "media exists" depends on the status of the recorder only
    @Trace(log)
    def create_media(self):
        if self.rec_id is not None:
            # the callback functions shouldn't call create_media if media already exists
            raise Ux("create_media: media already exists")
        my_uri = self.call.info().account.info().uri
        log.debug("%s: creating media" % my_uri)
        rec_file = "%srec_%s.wav" % (wav_dir, lib.uri_number(my_uri))
        log.debug("%s: pwd = %s" % (my_uri, getcwd()))
        log.debug("%s: rec file = %s" % (my_uri, rec_file))
        self.rec_id = lib.create_recorder(rec_file)
        self.rec_slot = lib.recorder_get_slot(self.rec_id)
        log.debug("%s: created recorder %s at slot %d" % (my_uri, self.rec_id, self.rec_slot))
        log.debug("%s: getting pbfile" % my_uri)
        if type(pbfile_strings) == dict and my_uri in pbfile_strings:
            pbfile = pbfile_strings[my_uri]
            log.debug("%s: got pbfile %s" % (my_uri, pbfile))
            log.debug("%s: creating player with pbfile = %s" % (my_uri, pbfile))
            self.player_id = lib.create_player(pbfile, loop=True)
            self.pb_slot = lib.player_get_slot(self.player_id)
            log.debug("%s: creating player %s at slot %d" % (my_uri, self.player_id, self.pb_slot))
            self.old_pbfile = pbfile
        else:
            log.debug("%s: pbfile not defined, no player created" % my_uri)

    @Trace(log)
    def patch_recfile(self, rec_file_name):
        # patch the wav file by adding size fields so wave module won't reject file
        #    (pjsip is supposed to do this when recorder is destroyed, but doesn't)
        f = open(rec_file_name, 'r+b')
        flen = len(f.read())
        f.seek(4)
        f.write(struct.pack('I', flen - 8))
        f.seek(40)
        f.write(struct.pack('I', flen - 44))
        f.close()

    @Trace(log)
    def destroy_media(self):
        if self.rec_id is None:
            raise Ux("destroy_media: no media exists")
        my_uri = self.call.info().account.info().uri
        log.debug("[destroy_media]%s: destroying media" % my_uri)
        lib.recorder_destroy(self.rec_id)
        self.rec_id = None
        rec_file_name = "%srec_%s.wav" % (wav_dir, lib.uri_number(my_uri))
        self.patch_recfile(rec_file_name)
        if self.player_id is not None:
            lib.player_destroy(self. player_id)
            self.player_id = None

    @Trace(log)
    def connect_media(self):
        global recorder_call_cbs
        if self.rec_id is None:
            raise Ux("connect_media: no media exists")
        self.rec_slot = lib.recorder_get_slot(self.rec_id)
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
        recorder_call_cbs[my_uri] = self
        # if there is a player ID then the player was created during create_media and we can connect it, too
        if self.player_id is not None:
            self.pb_slot = lib.player_get_slot(self.player_id)
            log.debug("%s: connecting player %s at slot %d to call slot %d"
                      % (my_uri, self.player_id, self.pb_slot, self.call.info().conf_slot))
            lib.conf_connect(self.pb_slot, self.call.info().conf_slot)
        self.media_call_slot = self.call.info().conf_slot
        # lib.reconnect_monitor(my_uri)

    @Trace(log)
    def restart_recorder(self, save_filename):
        """
        restarts the audio recorder for the parent uri;
        if save_filename is None, discards the recording made to this point;
        if save_filename is not None, saves the recording made to this point using that filename
        """
        if self.rec_id is None:
            raise Ux("restart_recorder: no recorder exists")
        my_uri = self.call.info().account.info().uri
        if self.media_call_slot is not None:
            self.rec_slot = lib.recorder_get_slot(self.rec_id)
            log.debug("%s: disconnecting recorder %s at slot %d from call slot %d"
                      % (my_uri, self.rec_id, self.rec_slot, self.media_call_slot))
            lib.conf_disconnect(self.media_call_slot, self.rec_slot)
        lib.recorder_destroy(self.rec_id)
        rec_file_name = "%srec_%s.wav" % (wav_dir, lib.uri_number(my_uri))
        self.patch_recfile(rec_file_name)
        if save_filename is not None:
            save_filepath = wav_dir + save_filename
            log.debug("%s: saving filename at %s" % (my_uri, save_filepath))
            try:
                remove(save_filepath)
            except:
                pass
            rename(rec_file_name, save_filepath)
        self.rec_id = lib.create_recorder(rec_file_name)
        self.rec_slot = lib.recorder_get_slot(self.rec_id)
        log.debug("%s: created recorder %s at slot %d" % (my_uri, self.rec_id, self.rec_slot))
        if self.media_call_slot is not None:
            log.debug("%s: connecting call slot %d to recorder %s at slot %d"
                      % (my_uri, self.media_call_slot, self.rec_id, self.rec_slot))
            lib.conf_connect(self.media_call_slot, self.rec_slot)

    # def disconnect_media(self):
    #     global recorder_call_cbs
    #     if self.rec_id is None:
    #         raise Ux("disconnect_media: no media exists")
    #     if self.media_call_slot is None:
    #         raise Ux("disconnect_media: media not connected")
    #     my_uri = self.call.info().account.info().uri
    #     log.debug("%s: disconnecting recorder %s at slot %d from call slot %d" %
    #           (my_uri, self.rec_id, self.rec_slot, self.media_call_slot))
    #     lib.conf_disconnect(self.media_call_slot, self.rec_slot)
    #     if my_uri in recorder_call_cbs:
    #         del recorder_call_cbs[my_uri]
    #     if self.player_id is not None:
    #         if self.pb_slot is None:
    #             raise Ux("disconnect media: no player slot")
    #         log.debug("%s: disconnecting player %s at slot %d from call slot %d" % (
    #             my_uri, self.player_id, self.pb_slot, self.media_call_slot))
    #         lib.conf_disconnect(self.media_call_slot, self.pb_slot)
    #     self.media_call_slot = None

    @Trace(log)
    def on_state(self):
        """Notification when call state has changed"""
        global current_calls
        global monitor_uri
        my_uri = self.call.info().account.info().uri
        if self.call.info().state == pj.CallState.DISCONNECTED and my_uri in current_calls:
            del current_calls[my_uri]
        else:
            current_calls[my_uri] = self.call
        remote_uri = re.match('<?([^>]+)', self.call.info().remote_uri).group(1)
        call_uri = re.match('<?([^>]+)', self.call.info().uri).group(1)
        log.debug("%s: ci.uri=%s ci.remote_uri=%s state %s media_state %s" % (
            my_uri, call_uri, remote_uri, self.call.info().state_text, media_state_text[self.call.info().media_state]))
        if cmd_q is not None:
            cmd_q.put("call %s %s ==> %s" % (call_state_text[self.call.info().state], my_uri, remote_uri))
            # if self.call.info().state == pj.CallState.CALLING:
            #     current_calls[my_uri] = self.call
        cmstate = (self.call.info().state == pj.CallState.CONFIRMED, self.call.info().media_state == pj.MediaState.ACTIVE)
        # if self.call_state == 'hold':
        #     log.debug("%s: old state = hold, cmstate = (%s, %s)" % (my_uri, cmstate[0], cmstate[1]))
        new_call_states = {
            'idle': {
                (False, False): 'idle',
                (False, True): 'pending',
                (True, False): 'pending',
                (True, True): 'call',
            },
            'pending': {
                (False, False): 'idle',
                (False, True): 'pending',
                (True, False): 'pending',
                (True, True): 'call',
            },
            'call': {
                (False, False): 'idle',
                (False, True): 'idle',
                (True, False): 'hold',
                (True, True): 'call',
            },
            'hold': {
                (False, False): 'idle',
                (False, True): 'idle',
                (True, False): 'hold',
                (True, True): 'call',
            }
        }
        new_call_state = new_call_states[self.call_state][cmstate]
        if cmd_q is not None:
            cmd_q.put("%s state=%s remote=%s" % (my_uri, new_call_state, remote_uri))
        transition = (self.call_state, new_call_state)
        log.debug("%s: transition %s --> %s" % (my_uri, transition[0], transition[1]))
        if transition == ('idle', 'call') or transition == ('pending', 'call'):
            self.create_media()
            self.connect_media()
            # current_calls[my_uri] = self.call
            if cmd_q is not None:
                cmd_q.put("call start %s ==> %s" % (my_uri, remote_uri))
        elif transition == ('call', 'hold'):
            self.media_call_slot = None
        elif transition == ('hold', 'call') or transition == ('call', 'call'):
            self.connect_media()
        elif transition[0] != 'idle' and transition[1] == 'idle':
            self.destroy_media()
            if my_uri == monitor_uri:
                monitor_uri = None
            self.media_call_slot = None
            # if my_uri in current_calls:
            #     del current_calls[my_uri]
            if cmd_q is None:
                log.debug("%s: cmd_q is None"%my_uri)
            else:
                log.debug("%s: putting call end %s ==> %s into queue" % (my_uri, my_uri, remote_uri))
                cmd_q.put("call end %s ==> %s" % (my_uri, remote_uri))
        self.call_state = new_call_state

    @Trace(log)
    def on_media_state(self):
        self.on_state()

    @Trace(log)
    def on_dtmf_digit(self, digits):
        my_uri = self.call.info().account.info().uri
        log.debug("%s - DTMF received: " % my_uri + digits)


class PjsuaLib(pj.Lib):
    @Trace(log)
    def __init__(self, quality=10, tx_drop_pct=0, rx_drop_pct=0):
        global monitor_uri
        global current_calls
        global recorder_call_cbs
        pj.Lib.__init__(self)
        self.quality = quality
        self.tx_drop_pct = tx_drop_pct
        self.rx_drop_pct = rx_drop_pct
        monitor_uri = None
        recorder_call_cbs = {}
        self.tcp = False

    def __del__(self):
        pass

    @Trace(log)
    def connect_monitor(self, new_monitor_uri):
        global monitor_uri
        log.debug(" monitor_uri = " + repr(monitor_uri))
        log.debug(" new_monitor_uri = " + repr(new_monitor_uri))
        if monitor_uri is not None:
            conf_slot = current_calls[monitor_uri].info().conf_slot
            lib.conf_disconnect(0, conf_slot)
            lib.conf_disconnect(conf_slot,0)
            monitor_uri = None
        if new_monitor_uri is not None and new_monitor_uri in current_calls:
            conf_slot = current_calls[new_monitor_uri].info().conf_slot
            lib.conf_connect(0, conf_slot)
            lib.conf_connect(conf_slot,0)
            monitor_uri = new_monitor_uri

    @Trace(log)
    def start(self, log_cb=pjl_log_cb, null_snd=False, tcp=False, dns_list=[]):
        try:
            self.tcp = tcp
            my_ua_cfg=pj.UAConfig()
            my_ua_cfg.max_calls = 8
            my_media_cfg = pj.MediaConfig()
            my_media_cfg.tx_drop_pct = self.tx_drop_pct
            my_media_cfg.rx_drop_pct = self.rx_drop_pct
            my_media_cfg.quality = self.quality
            my_media_cfg.ptime = 20
            if len(dns_list):
                my_ua_cfg.nameserver = dns_list
            self.init(log_cfg=pj.LogConfig(level=4, callback=log_cb), ua_cfg=my_ua_cfg, media_cfg=my_media_cfg)
            if self.tcp:
                transport = self.create_transport(pj.TransportType.TCP, pj.TransportConfig())
            else:
                transport=self.create_transport(pj.TransportType.UDP, pj.TransportConfig())
            log.debug("Listening on %s:%s"%(transport.info().host, transport.info().port))
            pj.Lib.start(self)
            if null_snd:
                self.set_null_snd_dev()
            # else:
            #    self.set_snd_dev(5,5)
            self.set_codec_priority('PCMU/8000/1',150)
            self.set_codec_priority('PCMU/8000/1',149)
            self.set_codec_priority('G722/16000/1',148)
            # lib.conf_connect(0,0)
        except pj.Error, e:
            raise Ux(pj_err_decode(e))

    @Trace(log)
    def uri_number(self, uri):
        return str(re.match('sip:([^@]+)', uri).group(1))

    @Trace(log)
    def uri_domain(self, uri):
        return str(re.match('sip:\d+@(.*)', uri).group(1))

    @Trace(log)
    def add_account(self, uri, proxy, pw=None):
        try:
            acc_cfg = pj.AccountConfig()
            acc_cfg.id = str(uri)
            acc_cfg.reg_uri = "sip:%s"%proxy
            acc_cfg.proxy = ["sip:%s"%proxy]
            acc_cfg.allow_contact_rewrite=False
            acc_cfg.auth_cred = [pj.AuthCred(realm="*", username=self.uri_number(uri), passwd=pw)]
            acc_cb = MyAccountCallback()
            acc = self.create_account(acc_cfg)
            acc.set_callback(acc_cb)
            acc_cb.wait()
            log.debug(("%s Registration complete, status=%s (%s)" %
                       (uri, acc.info().reg_status, acc.info().reg_reason)))
            return acc
        except pj.Error as e:
            sleep(1)
            txt = pj_err_decode(e)
            log.debug("Exception: " + txt)
            raise Ux(txt)

    @Trace(log)
    def restart_recorder(self, uri, save_filename=None):
        """ look up the call callback for uri and call the restart_recorder member function;

        uri -- the recorder for this account will be restarted
        save_filename -- the recording to this point will be saved with this name
            if save_filename is None, discards the recording made to this point;
            if save_filename is not None, saves the recording made to this point using that filename
        """
        if uri in recorder_call_cbs:
            recorder_call_cbs[uri].restart_recorder(save_filename)

lib = PjsuaLib()
