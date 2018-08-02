import six
import re
from time import localtime, strftime


def process_log(srcpath="log/service.log", destpath="log/webdriver.log", verbose=False):
    re_time = re.compile('\[(\d+)\.(\d+)')
    with open(srcpath) as src:
        with open(destpath, 'w') as dest:
            lines = src.readlines()
            in_cmd = False
            in_resp = False
            last = False
            for line in lines:
                line = line.rstrip()
                if line.find('COMMAND') != -1:
                    in_cmd = True
                    first = True
                    if verbose:
                        six.print_('')
                    dest.write('\n')
                elif line.find('RESPONSE') != -1:
                    in_resp = True
                    first = True
                else:
                    first = False
                if first:
                    sec, ms = re_time.match(line).groups()
                    timestamp = strftime('%m/%d/%y %H:%M:%S', localtime(int(sec))) + '.' + ms
                    line = re_time.sub(timestamp, line)
                if in_cmd or in_resp:
                    if len(line) > 0 and ((line[0] != ' ' and line[-1] != '{') or line[0] == '}'):
                        last = True
                    if verbose:
                        six.print_(line)
                    dest.write(line + '\n')
                if last:
                    in_cmd = False
                    in_resp = False
                    last = False


if __name__ == "__main__":
    process_log(verbose=True)
