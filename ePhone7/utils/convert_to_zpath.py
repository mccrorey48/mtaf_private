import re

from lib.android import get_abbrev

# read in the update_r2d2_orig.py script and print to stdout with xpaths converted to zpath,
# for reference in helping construct a script that uses the r2d2 test framework helpers;
# the resulting output is a python script that won't actually run because the webdriver
# find_element_by_xpath function doesn't understand zpaths
re_quoted = re.compile('([^"]*")(//[^"]+)(.*)')
re_suffix = re.compile('([^\[]+)(\[\d+\])')
with open('update_r2d2_orig.py') as f:
    lines = f.readlines()
    for line in lines:
        mq = re_quoted.match(line)
        if mq:
            xpath = mq.group(2)
            els = xpath.split('/')
            zp_els = []
            for el in els:
                ms = re_suffix.match(el)
                if ms:
                    zp_els.append(get_abbrev(ms.group(1)) + ms.group(2))
            print mq.group(1) + '/'.join(zp_els) + mq.group(3)
        else:
            print line,
