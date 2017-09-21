from matplotlib import pyplot as pl
import re
blf_re = re.compile('(?P<time>\d\d:\d\d:\d\d\.\d\d\d): \[(?P<user>\d\d\d\d)\] (?P<status>\S+)')
reg_re = re.compile('\S+\s(?P<time>\S+).*sip:(?P<user>\d+)@.*on_reg_state.*= 200')
state_re = re.compile('\S+\s(?P<time>\S+).*=sip:(?P<user>\d+)@\S+\sstate\s(?P<state>\S+)\smedia_state\s(?P<media_state>\S+)')


def ms(timestamp):
    [h, m, s, ms] = [int(x) for x in re.split('\D', timestamp)]
    return h*3600*1000 + m*60*1000 + s*1000 + ms


def get_user_blfs():
    _user_blfs = {}
    with open('log/blf_updates.log') as f:
        blf_lines = f.readlines()
    for line in blf_lines:
        m = blf_re.match(line)
        if m:
            (time, user, status) = m.groups()
            if status == 'alerting':
                status = 'progressing'
            if user not in _user_blfs:
                _user_blfs[user] = {status: [time]}
            elif status not in _user_blfs[user]:
                _user_blfs[user][status] = [time]
            else:
                _user_blfs[user][status].append(time)
    return _user_blfs


def get_user_logs():
    _user_logs = {}
    with open('log/esi_debug.log') as f:
        dbg_lines = f.readlines()
    for lnum, line in enumerate(dbg_lines):
        m = reg_re.match(line)
        if m:
            (time, user) = m.groups()
            if user not in _user_logs:
                _user_logs[user] = {'registered': [time]}
            elif 'registered' not in _user_logs[user]:
                _user_logs[user]['registered']= [time]
            else:
                _user_logs[user]['registered'].append(time)
            continue
        m = state_re.match(line)
        if m:
            (time, user, state, media_state) = m.groups()
            if state == 'EARLY':
                new_state = 'early'
            elif state == 'CONFIRMED' and media_state == 'ACTIVE':
                new_state = 'call'
            elif state == 'CONFIRMED' and media_state == 'NULL':
                new_state = 'hold'
            elif state == 'DISCONNECTED':
                new_state = 'idle'
            else:
                new_state = 'progressing'
            if user not in _user_logs:
                _user_logs[user] = {new_state: [time]}
            elif new_state not in _user_logs[user]:
                _user_logs[user][new_state]= [time]
            else:
                _user_logs[user][new_state].append(time)
    return _user_logs


user_blfs = get_user_blfs()
user_logs = get_user_logs()
reg_ms = [ms(user_blfs[user]['open'][0]) - ms(user_logs[user]['registered'][0]) for user in user_blfs]
# prog_ms = [ms(user_blfs[user]['progressing'][0]) - ms(user_logs[user]['progressing'][0]) for user in user_blfs]
call_ms = [ms(user_blfs[user]['inuse'][0]) - ms(user_logs[user]['call'][0]) for user in user_blfs]
idle_ms = [ms(user_blfs[user]['open'][-1]) - ms(user_logs[user]['idle'][0]) for user in user_blfs]
print len(reg_ms)
# print prog_ms
# print call_ms
# print idle_ms
pl.hist(reg_ms, bins=50, range=(0,8000), facecolor='blue', alpha=0.5, label='registered')
# pl.hist(prog_ms, bins=50, range=(0,8000), facecolor='green', alpha=0.5, label='progressing')
pl.hist(call_ms, bins=50, range=(0,8000), facecolor='red', alpha=0.5, label='in use')
pl.hist(idle_ms, bins=50, range=(0,8000), facecolor='brown', alpha=0.5, label='call ended')
pl.legend(loc='upper right')
pl.ylabel('number of samples')
pl.xlabel('Time interval from SIP event to BLF received')
pl.show()
