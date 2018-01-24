from mtaf.inspector.inspector import run_inspector
import sys
from os import getenv, path
from mtaf.lib.user_exception import UserException as Ux
from yaml import load, Loader
import platform


def start():
    # default is to use temporary directory for:
    #   inspector.png - screenshot
    #   inspector.xml - xml dump of display elements
    #   inspector.csv - conversion of xml xpaths to zpaths, element info in csv format
    #   inspector_locators.json - history of locators used to find elements from inspector
    # temporary directory is set by mtaf-inspector command line argument "tmp_dir=<path>", if it exists;
    # else, the value of environment variable "MTAF_TMP_DIR", if it exists;
    # else, platform-dependent temporary directory is used:
    #    Linux - /tmp
    #    Windows - os.getenv('TMP')
    #    Darwin - /tmp
    #
    # note: log directory is set in mtaf_logging module from MTAF_LOG_DIR environment variable, defaults to ./log
    system = platform.system()
    if system in ['Darwin', 'Linux']:
        tmp_dir = path.join('/tmp', 'MtafInspector')
    elif system == 'Windows':
        tmp_dir = path.join(getenv('TMP'), 'MtafInspector')
    else:
        raise Ux('Unknown system type %s' % system)
    cfg = {'tmp_dir': tmp_dir}
    # if there is a file "config.yml" in tmp_dir, add its settings to cfg
    try:
        with open(path.join(tmp_dir, 'config.yml')) as f:
            cfg2 = load(f, Loader=Loader)
        cfg.update(cfg2)
    except IOError:
        pass
    progname = path.basename(sys.argv[0])
    args = sys.argv[1:]
    for arg in args:
        terms = arg.split('=')
        if len(terms) != 2:
            raise Ux("arguments to %s must be of the form <key>=<value>, with no spaces" % progname)
        cfg[terms[0]] = terms[1]
    run_inspector(cfg)
