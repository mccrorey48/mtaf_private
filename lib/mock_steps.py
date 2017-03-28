import re
from lib.user_exception import UserException as Ux

step_re = re.compile('''@[^(]+\(['"](.+)['"]\)''')
def_re = re.compile('\s*def\s')
pass_re = re.compile('\s*pass')
comment_re = re.compile('\s*#')
exec_steps_re = re.compile('\s*context\.execute_steps')
end_exec_steps_re = re.compile("\s*'''\)")
fake_re = re.compile("\s*'''\)")

def find_mocks(filename, fake_tag=False):
    print "filename is " + filename
    is_mock = {}
    current_key = None
    quoted = False
    fake = False
    with open(filename) as f:
        lines = f.readlines()
        for lnum, line in enumerate(lines):
            if '"""' in line:
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
                fake = False
                current_key = step_key
            else:
                if 'fake' in line:
                    if fake_tag:
                        fake = True
                    continue
                if fake:
                    continue
                if current_key and len(line.strip()):
                    if not (('def' in line) or ('pass' in line) or comment_re.match(line)):
                        is_mock[current_key] = False
    mock_steps = []
    for key in sorted(is_mock.keys()):
        if is_mock[key]:
            mock_steps.append(key)
        # else:
        #     print "not mocked: %s" % key
    return mock_steps


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    args = parser.parse_args()
    if args.filename:
        find_mocks(args.filename)