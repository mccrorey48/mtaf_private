from mtaf.inspector.inspector import run_inspector
import sys
from mtaf.lib.user_exception import UserException as Ux


def start():
    args = sys.argv[1:]
    cfg = {}
    for arg in args:
        terms = arg.split('=')
        if len(terms) != 2:
            raise Ux("arguments to start() must be of the form <key>=<value>, with no spaces")
        cfg[terms[0]] = terms[1]
    run_inspector(cfg)
