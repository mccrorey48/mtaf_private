# from time import sleep
# from svauto.user_exception import UserException as Ux
import argparse
from time import sleep

import lib.logging_esi as logging_esi
from ePhone7.utils.configure import cfg
from ePhone7.utils.get_softphone import get_softphone

parser = argparse.ArgumentParser()
parser.add_argument("site_tag", type=str, choices=['mm', 'js', 'local'], help="specify site tag")
args = parser.parse_args()
cfg.set_site(args.site_tag)

from ePhone7.views.prefs import prefs_view
from ePhone7.views.user import user_view


def make_softphone_call():
    with logging_esi.msg_src_cm('make_softphone_call()'):
        softphone = get_softphone()
        dst_cfg = cfg.site['Accounts']['R2d2User']
        dst_uri = 'sip:' + dst_cfg['UserId'] + '@' + dst_cfg['DomainName']
        softphone.make_call_to_softphone(dst_uri)
        softphone.wait_for_call_status('early', 30)
        sleep(5)
        softphone.teardown_call()


def make_softphone_call_and_answer():
    with logging_esi.msg_src_cm('make_softphone_call()'):
        softphone = get_softphone()
        dst_cfg = cfg.site['Accounts']['R2d2User']
        dst_uri = 'sip:' + dst_cfg['UserId'] + '@' + dst_cfg['DomainName']
        softphone.make_call_to_softphone(dst_uri)
        softphone.wait_for_call_status('early', 30)
        user_view.actions.click_element_by_name('IncomingCallAnswerToSpeaker')
        softphone.wait_for_call_status('start', 30)
        sleep(5)
        # user_view.actions.click_element_by_name('EndActiveCall')
        # sleep(5)
        softphone.teardown_call()

user_view.update_remote('main')
# user_view.wait_for_view()
user_view.goto_prefs()
prefs_view.exit_prefs()
# user_view.wait_for_view()
make_softphone_call_and_answer()
# make_softphone_call()
# user_view.wait_for_view()
user_view.goto_tab('Contacts')

# if remote.driver.current_activity == ".activities.MainViewActivity":
#     user_view.logout()
# if remote.driver.current_activity == ".settings.ui.LoginActivity":
#     login_view.login()
# sleep(10)
# print "current activity = %s" % remote.driver.current_activity
# if remote.driver.current_activity == ".settings.ui.TermsAndConditionsScreen":
#     tnc_view.accept_tnc()
# sleep(10)
# print "current activity = %s" % remote.driver.current_activity


# # set up communication with the Appium server
# remote.update_remote('main')
# user_view.goto_tab('History')
# history_view.goto_tab('All')
# remote.update_remote('main')
# user_view.goto_tab('History')
# history_view.goto_tab('Missed')

# def call_first_history_entry():
#     elems = history_view.actions.find_elements('CallerName')
#     if len(elems) == 0:
#         raise Ux('No CallerName elements found')
#     name_elem = elems[0]
#     loc_y = name_elem.location['y']
#     print "first name location y = %s" % loc_y
#     entry_elems = history_view.actions.find_elements('HistoryEntry')
#     for i, entry_elem in enumerate(entry_elems[:-1]):
#         if entry_elems[i].location['y'] < loc_y < entry_elems[i+1].location['y']:
#             entry_elem = entry_elems[i]
#             break
#     else:
#         raise Ux('No HistoryEntry element found in same row as first CallerName element')
#     print "history entry location y = %s" % entry_elem.location['y']
#     call_icon = history_view.actions.find_sub_element(entry_elem, 'CallIcon')
#     print "call icon location y = %s" % call_icon.location['y']
#     call_icon.click()


# call_first_history_entry()
# pass

# try:
#     # elem = remote.find_element_with_timeout('id', 'com.esi_estech.com:id/call_log_empty', timeout=1)
#     # elem = remote.driver.find_element_by_id('com.esi_estech.ditto:id/call_log_empty')
#     elems = remote.driver.find_elements_by_xpath('com.esi_estech.ditto:id/call_log_empty')
# except BaseException as e:
#     print "%03d: Exception: %s" % (tries, e.msg)
#     continue
# else:
#     print "%03d: Found   is_displayed = %s" % (tries, elem.is_displayed())
# finally:
#     sleep(1)

