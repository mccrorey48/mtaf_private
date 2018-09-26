import re
from os import mkdir, getcwd
import contextlib
from cStringIO import StringIO
import sys
from behave.__main__ import main
import json


@contextlib.contextmanager
def capture():
    import sys
    oldout, olderr = sys.stdout, sys.stderr
    out = []
    try:
        out = [StringIO(), StringIO()]
        sys.stdout, sys.stderr = out
        yield out
    finally:
        sys.stdout, sys.stderr = oldout, olderr
        out[0] = out[0].getvalue()
        out[1] = out[1].getvalue()


def run_features(config):
    # make sure the tmp directory exists so we can put temporary files there
    try:
        mkdir('tmp')
    except OSError:
        pass
    sys.argv = [re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])]
    if 'run_tags' in config:
        sys.argv.append('--tags=%s' % config['run_tags'])
    if config.get('stop', False):
        sys.argv.append('--stop')
    sys.argv.append('-f')
    sys.argv.append('json.pretty')
    sys.argv.append(config.get('features_dir', 'features'))
    main()
    with capture() as out:
        main()

    data = json.loads('\n'.join(out[0][:out[0].rindex(']') + 1].split('\n')))
    print '<testsuites>'
    for feature in data:
        print '    <testsuite name="%s" tests="%d" failures="%d" errors="%d" skipped="%d" timestamp="%s" time="%s">' % (
            feature['name'],0, 0, 0, 0, 'timestamp', 'time')

        for scenario in feature['elements']:
            print '        <testcase name="%s">' % scenario['name']
            msg=''
            for step in scenario['steps']:
                print "    %s" % step['name']
            print '        </testcase>'
        print '    </testsuite>'
    print '</testsuites>'


if __name__ == "__main__":
    print "cwd = %s" % getcwd()
    run_features({})
