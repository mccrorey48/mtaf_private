import re
from lib.user_exception import UserException as Ux

step_re = re.compile('''@[^(]+\(['"](.+)['"]\)''')
def_re = re.compile('def\s+([^(]+)(.+)')


def sort(filename):
    print "filename is " + filename
    step_defs = {}
    prefix_lines = []
    current_key = None
    with open(filename) as f:
        lines = f.readlines()
        for lnum, line in enumerate(lines):
            m = step_re.match(line)
            if m:
                step_key = m.group(1).lower().translate(None, '''"'{}_-!/,''')
                step_key = '_'.join(step_key.split())
                if step_key in step_defs:
                    raise Ux("duplicate step name on line %s" % (lnum + 1) )
                else:
                    step_defs[step_key] = [line]
                current_key = step_key
            else:
                if current_key is None:
                    prefix_lines.append(line)
                elif def_re.match(line):
                    arglist = def_re.match(line).group(2)
                    step_defs[current_key].append('def ' + current_key + arglist + '\n')
                elif len(line.strip()):
                    step_defs[current_key].append(line)
    with open(filename, 'w') as f:
        for line in prefix_lines:
            f.write(line)
        for key in sorted(step_defs.keys(), key=lambda key: ''.join(key.lower().split('"'))):
            # print ">>> " + key
            for line in step_defs[key]:
                f.write(line)
            f.write("\n\n")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    args = parser.parse_args()
    if args.filename:
        sort(args.filename)