from ePhoneGoAndroid.utils.configure import cfg
from ePhoneGoAndroid.views import *


def before_all(context):
    site_tag = context.config.userdata.get('site_tag')
    if 'cfg_server' in context.config.userdata:
        cfg_server = context.config.userdata.get('cfg_server')
    else:
        cfg_server = 'vqda'
    cfg.set_site(cfg_server, site_tag)
    base_view.open_appium('settings')
    pass
    # if login_view.element_is_present('AttentionAlertMessage'):
    #     login_view.click_element_by_name('AttentionOkButton')
    # if login_view.element_is_present('PhonePermissionAlertTitle'):
    #     login_view.click_element_by_name('PermissionAllowButton')
    # if login_view.element_is_present('RecordAudioAlertMessage'):
    #     login_view.click_element_by_name('PermissionAllowButton')
    # if login_view.element_is_present('AccessContactsAlertTitle'):
    #     login_view.click_element_by_name('PermissionAllowButton')
    # if login_view.element_is_present('AccessMediaAlertTitle'):
    #     login_view.click_element_by_name('PermissionAllowButton')
    # if login_view.element_is_present('AccessLocationAlertTitle'):
    #     login_view.click_element_by_name('PermissionAllowButton')
    # if login_view.element_is_present('FunctionalityAlertTitle'):
    #     login_view.click_element_by_name('AttentionOkButton')
    settings_view.scroll_and_get_element("Storage").click()
    pass
    # storage_view.scroll_and_get_element("Apps").click()
    # storage_view.scroll_and_get_element("ePhoneGo").click()
    # storage_view.click_element_by_name("ClearData")
    # storage_view.click_element_by_name("Delete")



def after_all(context):
    base_view.close_appium()
