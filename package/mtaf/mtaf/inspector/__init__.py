from mtaf.inspector.inspector import run_inspector
import sys
from os import getenv, path
from mtaf.lib.user_exception import UserException as Ux


def start():
    # default is to use temporary directory for:
    #   inspector.png - screenshot
    #   inspector.xml - xml dump of display elements
    #   inspector.csv - conversion of xml xpaths to zpaths, element info in csv format
    #   inspector_locators.json - history of locators used to find elements from inspector
    # temporary directory is set by mtaf-inspector command line argument "tmp_dir=<path>", if it exists;
    # else, the value of environment variable "MTAF_TMP_DIR", if it exists;
    # else, "~/.MtafInspector"
    # note: log directory is set in mtaf_logging module from MTAF_LOG_DIR environment variable, defaults to ./log
    cfg = {
        'tmp_dir': getenv('MTAF_TMP_DIR', path.join(getenv('HOME'), '.MtafInspector'))
    }
    args = sys.argv[1:]
    for arg in args:
        terms = arg.split('=')
        if len(terms) != 2:
            raise Ux("arguments to start() must be of the form <key>=<value>, with no spaces")
        cfg[terms[0]] = terms[1]
    run_inspector(cfg)
