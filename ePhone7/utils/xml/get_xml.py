import argparse
import os

from selenium.common.exceptions import NoSuchElementException

from ePhone7.utils.configure import cfg

parser = argparse.ArgumentParser()
parser.add_argument("site_tag", type=str, choices=['mm', 'js', 'local', 'ds'], help="specify site tag")
args = parser.parse_args()

cfg.set_site(args.site_tag)
from lib.softphone.softphone import get_softphone
from ePhone7.views.user import user_view
from ePhone7.views.prefs import prefs_view
from ePhone7.views.base import base_view
from ePhone7.utils.csv.xml_to_csv import xml_folder_to_csv
from time import sleep
import lib.logging_esi as logging_esi
from ePhone7.utils.xml.view_info import view_info
from lib.wrappers import Trace
from lib.user_exception import UserException as Ux
log = logging_esi.get_logger('esi.get_xml')
logging_esi.console_handler.setLevel(logging_esi.TRACE)


@Trace(log)
def save_xml_and_screenshot(basename, version):
    with logging_esi.msg_src_cm('save_xml_and_screenshot()'):
        xml = base_view.get_source()
        xml_dir = os.path.join(cfg.xml_folder, 'xml_%s' % version)
        try:
            os.makedirs(xml_dir)
        except OSError as e:
            # ignore 'File exists' error but re-raise any others
            if e.errno != 17:
                raise e
        xml_fullpath = os.path.join(xml_dir, '%s.xml' % basename)
        log.info("saving xml %s" % xml_fullpath)
        with open(xml_fullpath, 'w') as _f:
            _f.write(xml.encode('utf8'))
        base_view.get_screenshot_as_png(basename, cfg.screenshot_folder)


@Trace(log)
def get_call_views(version):
    with logging_esi.msg_src_cm('get_page_sources()'):
        # user_view.goto_prefs()
        # prefs_view.set_auto_answer_off()
        # prefs_view.exit_prefs()
        softphone = get_softphone()
        dst_cfg = cfg.site['Accounts']['R2d2User']
        dst_uri = 'sip:' + dst_cfg['UserId'] + '@' + dst_cfg['DomainName']
        softphone.make_call(dst_uri)
        softphone.wait_for_call_status('early', 30)
        answer_to_speaker_icon = user_view.find_element_by_key('IncomingCallAnswerToSpeaker')
        save_xml_and_screenshot('incoming_call_%s' % version, version)
        user_view.click_element(answer_to_speaker_icon)
        softphone.wait_for_call_status('start', 30)
        sleep(5)
        # end_active_call = user_view.find_element_by_key('EndActiveCall')
        save_xml_and_screenshot('active_call_%s' % version, version)
        # log.trace("clicking end active call icon")
        # end_active_call.click()
        # log.trace("clicked end active call icon")
        # softphone.wait_for_call_status('end', 30)
        softphone.teardown_call()

@Trace(log)
def get_nav_views(version):
    with logging_esi.msg_src_cm('get_page_sources()'):
        # get the source for the prefs screen
        user_view.goto_prefs()
        save_xml_and_screenshot('prefs_%s' % version, version)
        prefs_view.exit_prefs()
        # navigate to the various view screens, get each view's xml source and save it
        for view in sorted(view_info):
            log.info("view = %s" % view)
            info = view_info[view]
            # for views that are selected with a bottom tab, there is a 'view_tab' attribute
            # designating the tab to be clicked by the 'user' view class to select that view
            if 'view_tab' in info:
                log.info("calling UserView.goto_tab(%s)" % info['view_tab'])
                user_view.goto_tab(info['view_tab'])
                # arbitrary sleep to give the screen time to switch
                sleep(5)
            # for each view grab the xml
            save_xml_and_screenshot("%s_%s" % (view, version), version)
            # for each tab in the view, grab a screenshot
            for tab in info['tabs']:
                tab_name = info['tabs'][tab]['locator_name']
                log.info("calling %s.goto_tab(%s)" % (info['view_classname'], tab_name))
                info['view_instance'].goto_tab(tab_name)
                sleep(5)
                save_xml_and_screenshot('%s_%s_%s' % (view, tab, version), version)


if __name__ == '__main__':
    _version = 'not_retrieved'
    # try:
    base_view.open_appium('main')
    user_view.goto_prefs()
    _version = prefs_view.get_app_version()
    prefs_view.exit_prefs()
    print "version = %s" % _version
    try:
        get_call_views(_version)
        base_view.close_appium()
        base_view.open_appium('main')
        get_nav_views(_version)
        base_view.close_appium()
    except Ux as _e:
        save_xml_and_screenshot('user_exception_handler', _version)
        log.warn('UserException: %s' % _e)
        pass
    except NoSuchElementException as _e:
        save_xml_and_screenshot('no_such_element_exception_handler', _version)
        log.warn('NoSuchElementException: %s' % _e)
    else:
        print "version = %s" % _version
        # just process all *.xml into *.csv
        xml_folder_to_csv()