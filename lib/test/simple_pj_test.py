import re
import time
# from matplotlib import pyplot as pl
get_new_data = False
if get_new_data:
    import lib.softphone.simple_pj as pj
    import lib.common.logging_esi as logging_esi
    log = logging_esi.get_logger('esi.simple_pj_test')
    # set console log level
    logging_esi.console_handler.setLevel(logging_esi.INFO)
    lib = pj.PjsuaLib()
    lib.start(dns_list=['10.0.50.156', '10.0.50.157'])
    lib.add_account('2202', 'customer4', 'nr5.cpbx.esihs.net', '1W6Rowrb')
    lib.add_account('2203', 'customer4', 'nr5.cpbx.esihs.net', 'wv6ocUgT')
    caller_info = lib.acct_infos['sip:2202@customer4']
    caller_info.call = caller_info.account.make_call('sip:2203@customer4')
    caller_info.call.set_callback(pj.MyCallCallback(caller_info))
    called_info = lib.acct_infos['sip:2203@customer4']
    send_180 = True
    for i in range(20):
        # if caller_info.call:
        #     log.info('call %s local %s remote %s' % (pj.call_state_text[caller_info.state],
        #                                              re.match('("[^"]*"\s+)?<?([^>]+)',
        #                                                       caller_info.call.info().uri).group(2),
        #                                              re.match('("[^"]*"\s+)?<?([^>]+)',
        #                                                       caller_info.call.info().remote_uri).group(2)))
        # else:
        #     log.info('no outgoing call')
        if called_info.call:
            # log.info('call %s local %s remote %s' % (pj.call_state_text[called_info.state],
            #                                          re.match('("[^"]*"\s+)?<?([^>]+)',
            #                                                   called_info.call.info().uri).group(2),
            #                                          re.match('("[^"]*"\s+)?<?([^>]+)',
            #                                                   called_info.call.info().remote_uri).group(2)))
            if send_180:
                # log.info('called answer(180)')
                called_info.call.answer(180)
                send_180 = False
            if i == 10:
                # log.info('called answer(200)')
                called_info.call.answer(200)
            if i == 15:
                # log.info('caller hanging up')
                caller_info.call.hangup()
        # else:
        #     log.info('no incoming call')
        time.sleep(1)
        # log.info('')
    lib.destroy()
    # x = range(1000)
    # y = range(1000)

re_trans = re.compile('(\S+\s+[^.]+)\.(\S+).*sip:([^@]+).*(call|media) transition .*-->\s+(.*)')
re_request = re.compile('(\S+\s+[^.]+)\.(\S+).*(Request) msg (\S+)\s+\S+\s+(to \S+\s+\S+):')
re_response = re.compile('(\S+\s+[^.]+)\.(\S+).*.*(Response) msg (\S+)\s+\S+\s+(from \S+\s+\S+):')
re_invite = re.compile('(\S+\s+[^.]+)\.(\S+).*(Request) msg (INVITE\S+)')
lines = []
start = None
start_secs = 0
with open('log/esi_debug.log', 'r') as f:
    for line in f:
        if line.find('REGISTER') > 0:
            continue
        if start:
            m_trans = re_trans.match(line)
            m_req = re_request.match(line)
            m_resp = re_response.match(line)
            m = m_trans or m_req or m_resp
            if m:
                t = time.strptime(m.group(1), "%m/%d/%y %H:%M:%S")
                secs = float(time.mktime(t)) + (float(m.group(2))/1000.0) - start_secs
                print "%.3f, %s, %s, %s" % (secs, m.group(3), m.group(4), m.group(5))
        else:
            m = re_invite.match(line)
            if m:
                start = time.strptime(m.group(1), "%m/%d/%y %H:%M:%S")
                start_secs = float(time.mktime(start)) + (float(m.group(2))/1000.0)
                print "%.3f %s %s" % (start_secs, m.group(3), m.group(4))

# pl.plot(x, y)
# pl.xlabel("Time in seconds")
# pl.grid(True)
# pl.axis([0, 1000, 0, 1000])
# pl.show()
