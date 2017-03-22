import re
from lib.user_exception import UserException as Ux

step_re = re.compile('''@[^(]+\(['"](.+)['"]\)''')
doc_re = re.compile('\s*"""')
def_re = re.compile('\s*def\s')
pass_re = re.compile('\s*pass')

def find_mocks(filename):
    print "filename is " + filename
    is_mock = {}
    current_key = None
    quoted = False
    with open(filename) as f:
        lines = f.readlines()
        for lnum, line in enumerate(lines):
            if doc_re.match(line):
                quoted = not quoted
                continue
            if quoted:
                continue
            m = step_re.match(line)
            if m:
                step_key = m.group(1).lower()
                # print step_key
                if step_key in is_mock:
                    raise Ux("duplicate step name on line %s" % (lnum + 1) )
                else:
                    is_mock[step_key] = True
                current_key = step_key
            else:
                if current_key and len(line.strip()):
                    if not (def_re.match(line) or pass_re.match(line)):
                        is_mock[current_key] = False
    mock_steps = []
    for key in sorted(is_mock.keys()):
        if is_mock[key]:
            mock_steps.append(key)
    return mock_steps


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    args = parser.parse_args()
    if args.filename:
        find_mocks(args.filename)