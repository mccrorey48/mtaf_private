import re
from os import mkdir
import contextlib


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
    sys.argv.append('-D')
    sys.argv.append('portal_server=%s' % config['portal_server'])
    sys.argv.append('-D')
    sys.argv.append('user_scope=%s' % config['user_scope'])
    sys.argv.append('--tags=%s' % config['user_scope'])
    if config['run_tags']:
        sys.argv.append('--tags=%s' % config['run_tags'])
    if config['stop']:
        sys.argv.append('--stop')
    sys.argv.append('-k')
    sys.argv.append('-f')
    sys.argv.append('json.pretty')
    sys.argv.append(config['features_dir'])
    with capture() as out:
        main()

    # save the output of behave (json test results plus plain text summary at the end)
    # for reference and debugging
    with open('tmp/main.out', 'w') as f:
        f.write(out[0])


if __name__ == "__main__":
    config = {}
    run_features(config)
