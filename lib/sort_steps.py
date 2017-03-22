import re
from lib.user_exception import UserException as Ux

step_re = re.compile('''@[^(]+\(['"](.+)['"]\)''')

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
                step_key = m.group(1).lower()
                # print step_key
                if step_key in step_defs:
                    raise Ux("duplicate step name on line %s" % (lnum + 1) )
                else:
                    step_defs[step_key] = [line]
                current_key = step_key
            else:
                if current_key is None:
                    prefix_lines.append(line)
                elif len(line.strip()):
                    step_defs[current_key].append(line)
    with open(filename, 'w') as f:
        for line in prefix_lines:
            f.write(line)
        for key in sorted(step_defs.keys()):
            # print ">>> " + key
            for line in step_defs[key]:
                f.write(line)
            f.write("\n")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    args = parser.parse_args()
    if args.filename:
        sort(args.filename)