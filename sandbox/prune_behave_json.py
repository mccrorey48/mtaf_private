import sys

if len(sys.argv) != 3:
    print "usage: %s <input file> <output file>"
    exit()

with open(sys.argv[1]) as f:
    out = f.read()
json_repr = '\n'.join(out[:out.rindex(']') + 1].split('\n'))
with open(sys.argv[2], 'w') as f:
    f.write(json_repr)
