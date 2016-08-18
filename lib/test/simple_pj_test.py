import re
import time
from matplotlib import pyplot as pl
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

dtms = '(?P<dt>\S+\s+[^.]+)\.(?P<ms>\S+)'
re_trans = re.compile(dtms + '.*sip:([^@]+).*(call|media) transition .*-->\s+(.*)')
re_request = re.compile(dtms + '.*(?P<type>Request) msg (?P<desc>\S+cseq=(?P<cseq>\d+))\s+\S+\s+(?P<dir>to|from)')
re_response = re.compile(dtms + '.*(?P<type>Response) msg (?P<desc>\S+cseq=(?P<cseq>\d+))\s+\S+\s+(?P<dir>to|from)')
re_invite = re.compile(dtms + '.*(Request) msg (INVITE\S+)')
lines = []
start = None
start_secs = 0
start_timestamp = ''
cseq_ds = {}
cseq_descs = {}
with open('log/esi_debug.log', 'r') as f:
    for i, line in enumerate(f):
        if line.find('REGISTER') > 0:
            continue
        if start:
            m_trans = re_trans.match(line)
            m_req = re_request.match(line)
            m_resp = re_response.match(line)
            m = m_trans or m_req or m_resp
            if m:
                timestamp = "%s.%s" % (m.group('dt'), m.group('ms'))
                t = time.strptime(m.group('dt'), "%m/%d/%y %H:%M:%S")
                secs = float(time.mktime(t)) + (float(m.group('ms'))/1000.0) - start_secs
                ms = int(secs * 1000)
                if m_req or m_resp:
                    cseq = m.group('cseq')
                    if cseq not in cseq_descs:
                        cseq_descs[cseq] = [m.group('desc')]
                    elif m.group('desc') in cseq_descs[cseq]:
                        # throw away repeats
                        continue
                    else:
                        cseq_descs[cseq].append(m.group('desc'))
                    print "%s %6.3f, %s, %s, %s, %s" % (m.group('dt'), secs, m.group('type'), m.group('desc'), m.group('cseq'), m.group('dir'))
                    d = {'ms': ms, 'timestamp': timestamp, 'secs': secs, 'type': m.group('type'), 'desc': m.group('desc'), 'dir': m.group('dir')}
                    if cseq in cseq_ds:
                        cseq_ds[cseq].append(d)
                    else:
                        cseq_ds[cseq] = [d]
                else:
                    print "%s %6.3f, %s, %s, %s" % (timestamp, secs, m.group(3), m.group(4), m.group(5))
        else:
            m = re_invite.match(line)
            if m:
                start_timestamp = m.group(1)
                start = time.strptime(start_timestamp, "%m/%d/%y %H:%M:%S")
                start_secs = float(time.mktime(start)) + (float(m.group(2))/1000.0)
                print "%.3f %s %s" % (start_secs, m.group(3), m.group(4))

max_t = 20000
x = range(max_t)
inv_offsets = {'INV': 0.5, '407': 0.4, '100': 0.3, '180': 0.2, '200': 0.1, 'ACK': 0.0}
bye_offsets = {'BYE': 0.1, '200': 0.0}
print start_timestamp
base_y = 0
for cseq in cseq_ds:
    base_y += 1
    cur_y = base_y
    y = []
    y_offsets = {}
    req_desc = cseq_ds[cseq][0]['desc']
    req_dir = cseq_ds[cseq][0]['dir']
    print "cseq %s" % cseq
    # if there are multiple d's for this cseq with the same timestamps, tweak the timestamps to space them at
    # 1 ms intervals so they will show up on the plot
    d_indices_by_ms = {}
    for i, d in enumerate(cseq_ds[cseq]):
        ms = d['ms']
        if ms in d_indices_by_ms:
            # print "appending %d at ms %d" % (i, ms)
            d_indices_by_ms[ms].append(i)
        else:
            # print "setting %d at ms %d" % (i, ms)
            d_indices_by_ms[ms] = [i]
    for ms in d_indices_by_ms:
        add_ms = 1
        for i in d_indices_by_ms[ms][1:]:
            cseq_ds[cseq][i]['ms'] += add_ms
            add_ms += 1
    for d in cseq_ds[cseq]:
        print "    %s %s %6.3f  %8s  %28s %s" % (d['ms'], d['timestamp'], d['secs'], d['type'], d['dir'], d['desc'])
        # get ms for start of new y value
        if req_desc[:6] == 'INVITE':
            y_offsets[d['ms']] = inv_offsets[d['desc'][:3]]
        elif req_desc[:3] == 'BYE':
            y_offsets[d['ms']] = bye_offsets[d['desc'][:3]]
    for ms in range(max_t):
        if ms in y_offsets:
            cur_y = base_y + y_offsets[ms]
            print "cseq %s: changing y to %.2f at ms=%d" % (cseq, cur_y, ms)
        y.append(cur_y)
        # in case two events happen on the same millisecond for this cseq, put one point so the first event will show
        # up on the plot
    pl.plot(x, y, label='hello')
    pl.text(max_t - 4000, base_y + 0.1, "%s %s" % (req_desc[:3], req_dir + ' PBX'))
pl.grid(True)
pl.axis([0, max_t, 0, base_y + 1])
pl.grid(True)
pl.xlabel("Time in milliseconds")
pl.yticks( range(1, len(cseq_ds) + 1), cseq_ds)
pl.ylabel("cseqs")
pl.show()
