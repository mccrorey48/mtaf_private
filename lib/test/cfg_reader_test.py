"""
test the cfg_reader module installed from svauto_shared
"""
from lib.common.cfg_reader import CfgReader
import pprint
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mongo_host", type=str, default='vqda',
                    help="(optional) specify mongodb host, default 'vqda'")
parser.add_argument("-s", "--svr_tag", type=str, default='test',
                    help="(optional) specify ccd server tag, default 'test'")
args = parser.parse_args()
pp = pprint.PrettyPrinter(indent=4)
cfg_reader = CfgReader(args.mongo_host)
cfg_reader.read_account_cfg_from_db(args.svr_tag, 'ccd', use_dtmf_audio=True)
cfg_reader.read_account_cfg_from_db(args.svr_tag, 'ccd', use_dtmf_audio=False)
print "account_configs:"
pp.pprint(cfg_reader.get_account_configs())
print "pbfile_strings:"
pp.pprint(cfg_reader.get_pbfile_strings())
cfg_reader.read_locators_from_db(args.svr_tag)
print args.svr_tag + " xpaths:"
pp.pprint(cfg_reader.get_locators()['xpath'])
print args.svr_tag + " javascript:"
pp.pprint(cfg_reader.get_locators()['javascript'])
print 'ini_tags:'
print '    production:', cfg_reader.get_ini_tags('production')
print '    svlab:', cfg_reader.get_ini_tags('svlab')
print '    asterisk:', cfg_reader.get_ini_tags('asterisk')
