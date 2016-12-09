import argparse

from ePhone7.utils.configure import cfg

parser = argparse.ArgumentParser()
parser.add_argument("site_tag", type=str, choices=['mm', 'js', 'mm_svlab'], help="specify site tag")
parser.add_argument('-c', '--cfg_host', help='name of mongodb server for test configuration, default "vqda"',
                    default='vqda')
args = parser.parse_args()
cfg.set_site(args.cfg_host, args.site_tag)

from ePhone7.utils.get_softphone import get_softphone
from time import sleep
import lib.logging_esi as logging_esi

log = logging_esi.get_logger('esi.softphone_test')
logging_esi.console_handler.setLevel(logging_esi.TRACE)
softphone = get_softphone('Auto TesterC')
softphone.make_call('sip:1000@SVAutoCustomer')
sleep(10)
softphone.end_call()
