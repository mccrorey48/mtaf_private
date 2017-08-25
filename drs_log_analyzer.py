import re
from matplotlib import pyplot as pl
corp_con_re = re.compile('(\d+)ms: (\[([^]]+)\]\["([^-]+)-([^"]+)",({[^{}]+}))')
start_ws_re = re.compile('(\d+)ms: starting websocket for user (.*)')
ws_starts = {}
payloads = {}
max_ms = 0
option_type = None

# configuration values
bin_size_ms = 500

with open('/home/mmccrorey/drs/drs_test.log') as f:
    lines = f.readlines()
for line in lines:
    if corp_con_re.match(line):
        (ms_str, all, user, option_type, domain, data) = corp_con_re.match(line).groups()
        ms = int(ms_str)
        length = len(all)
        # print "ms = %s" % ms
        # print "all = %s" % all
        # print "user = %s" % user
        # print "option_type = %s" % option_type
        # print "domain = %s" % domain
        # print "data = %s" % data
        max_ms = max(ms, max_ms)
        user_uri = user + '@' + domain
        if user_uri not in payloads.keys():
            payloads[user_uri] = {}
        if option_type not in payloads[user_uri]:
            payloads[user_uri][option_type] = {}
        if ms in payloads[user_uri][option_type]:
            payloads[user_uri][option_type][ms]["payload_size"] += length
            payloads[user_uri][option_type][ms]["data"] += data
        else:
            payloads[user_uri][option_type][ms] = {"payload_size": length, "data": data}
    elif start_ws_re.match(line):
        (ms_str, user_uri) = start_ws_re.match(line).groups()
        ms = int(ms_str)
        if ms not in ws_starts.keys():
            ws_starts[ms] = [user_uri]
        else:
            ws_starts[ms].append(user_uri)

bin_count = max_ms/bin_size_ms + 2
x = range(0, bin_count * bin_size_ms, bin_size_ms)
bytes_per_bin = [0 for _bin in range(bin_count)]
ws_starts_per_bin = [0 for __bin in range(bin_count)]

for user_uri in payloads.keys():
    for option_type in payloads[user_uri].keys():
        for ms in sorted(payloads[user_uri][option_type].keys()):
            ms_data = payloads[user_uri][option_type][ms]
            _bin = ms / bin_size_ms
            bytes_per_bin[_bin] += ms_data["payload_size"]
            print "%s %s %s ms: payload_size = %s" % (user_uri, option_type, ms, ms_data["payload_size"])
bps = [bytes_per_bin[_bin] * 1000 / bin_size_ms for _bin in range(bin_count)]

for ms in range(max_ms):
    if ms in ws_starts.keys():
        ws_starts_per_bin[ms / bin_size_ms] += len(ws_starts[ms])


fix, ax1 = pl.subplots()
ax1.plot(x, bps, 'b-')
ax1.set_xlabel('time(s)')
ax1.set_ylabel('bps', color='b')
ax1.tick_params('y', colors='b')
ax2 = ax1.twinx()
ax2.plot(x, ws_starts_per_bin, 'r-')
ax2.set_ylabel('websocket starts', color='r')
ax2.tick_params('y', colors='r')
pl.suptitle('DRS Throughput vs Time (%s)' % option_type)
# pl.xticks(range(0, bin_count * bin_size_ms, bin_size_ms))
pl.show()
