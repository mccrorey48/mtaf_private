import os

from selenium.common.exceptions import NoSuchElementException

from ePhone7.config.configure import cfg

from ePhone7.lib.utils.get_softphone import get_softphone
from ePhone7.views import *
from ePhone7.lib.utils.csv.xml_to_csv import xml_folder_to_csv
from time import sleep
from mtaf import mtaf_logging
from mtaf.trace import Trace
from mtaf.user_exception import UserException as Ux
log = mtaf_logging.get_logger('mtaf.get_xml')
logging_esi.console_handler.setLevel(logging_esi.TRACE)


@Trace(log)
def save_xml_and_screenshot(basename, version):
    with mtaf_logging.msg_src_cm('save_xml_and_screenshot()'):
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
    with mtaf_logging.msg_src_cm('get_page_sources()'):
        # user_view.goto_prefs()
        # prefs_view.set_auto_answer_off()
        # prefs_view.exit_prefs()
        softphone = get_softphone()
        dst_cfg = cfg.site['Users']['R2d2User']
        dst_uri = 'sip:' + dst_cfg['UserId'] + '@' + dst_cfg['DomainName']
        softphone.make_call(dst_uri)
        softphone.wait_for_call_status('early', 30)
        answer_to_speaker_icon = user_view.find_named_element('IncomingCallAnswerToSpeaker')
        save_xml_and_screenshot('incoming_call_%s' % version, version)
        user_view.click_element(answer_to_speaker_icon)
        softphone.wait_for_call_status('call', 30)
        sleep(5)
        # end_active_call = user_view.find_named_element('EndActiveCall')
        save_xml_and_screenshot('active_call_%s' % version, version)
        active_call_view.click_named_element('InCallDial')
        save_xml_and_screenshot('active_call_dial_%s' % version, version)
        # log.trace("clicking end active call icon")
        # end_active_call.click()
        # log.trace("clicked end active call icon")
        # softphone.wait_for_call_status('idle', 30)
        softphone.end_call()


buttons = {
    'Contacts': {'view': contacts_view, 'tabs': ['Personal', 'Coworkers', 'Favorites', 'Groups']},
    'History': {'view': history_view, 'tabs': ['All', 'Missed']},
    'Voicemail': {'view': voicemail_view, 'tabs': ['New', 'Saved', 'Trash']},
    'Dial': {'view': dial_view, 'tabs': []}
}

@Trace(log)
def get_nav_views(version):
    with mtaf_logging.msg_src_cm('get_page_sources()'):
        save_xml_and_screenshot('user_%s' % version, version)
        for button in ['Contacts', 'History', 'Voicemail', 'Dial']:
            user_view.goto_tab(button)
            log.info("view = %s" % button)
            if button == 'Dial':
                save_xml_and_screenshot('dial_%s' % version, version)
                dial_view.dial_named_number('Advanced Settings')
                dial_view.touch_dial_button()
                save_xml_and_screenshot('settings_%s' % version, version)
                dial_view.send_keycode_back()
            for tab in buttons[button]['tabs']:
                log.info("calling goto_tab(%s)" % tab)
                buttons[button]['view'].goto_tab(tab)
                # arbitrary sleep to give the screen time to switch
                sleep(5)
                log.info("tab = %s" % tab)
                save_xml_and_screenshot('%s_%s_%s' % (button.lower(), tab.lower(), version), version)


if __name__ == '__main__':
    _version = 'not_retrieved'
    # try:
    base_view.open_appium('nolaunch', force=True, timeout=60)
    base_view.startup()
    user_view.goto_prefs()
    _version = prefs_view.get_app_version()
    save_xml_and_screenshot('prefs_%s' % _version, _version)
    prefs_view.exit_prefs()
    print "version = %s" % _version
    try:
        get_call_views(_version)
        base_view.close_appium()
        base_view.open_appium('nolaunch', force=True, timeout=60)
        base_view.startup()
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
