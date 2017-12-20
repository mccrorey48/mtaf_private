from softphone_plugin import create_softphone_frame
from ePhone7.views import *
from ePhone7.utils.usb_enable import usb_enable
from ePhone7.utils.versions import get_installed_versions
from ePhone7.config.configure import cfg
from ePhone7.utils.spud_serial import SpudSerial
from ePhone7.utils.get_softphone import get_softphone


class E7Commands(object):

    def __init__(self, parent):
        self.parent = parent

    @staticmethod
    def dial_beta_ota():
        print "dialing beta OTA code...",
        user_view.goto_tab('Dial')
        user_view.touch_element_with_text('Dial')
        dial_view.dial_set_beta_ota_server()
        dial_view.touch_call_button()
        print "Done"

    @staticmethod
    def dial_alpha_ota():
        print "dialing alpha OTA code...",
        user_view.goto_tab('Dial')
        user_view.touch_element_with_text('Dial')
        dial_view.dial_set_alpha_ota_server()
        dial_view.touch_call_button()
        print "Done"

    @staticmethod
    def dial_prod_ota():
        print "dialing prod OTA code...",
        user_view.goto_tab('Dial')
        dial_view.dial_set_production_ota_server()
        dial_view.touch_call_button()
        print "Done"

    @staticmethod
    def dial_show_ota():
        print "dialing show OTA code...",
        user_view.goto_tab('Dial')
        dial_view.dial_show_ota_server()
        dial_view.touch_call_button()
        print "Done"

    @staticmethod
    def dial_advanced_settings():
        print "dialing advanced settings code...",
        user_view.goto_tab('Dial')
        dial_view.dial_advanced_settings()
        dial_view.touch_call_button()
        print "Done"

    @staticmethod
    def get_installed_versions():
        print "getting installed versions"
        # self.update_idletasks()
        aosp, app = get_installed_versions()
        print "aosp: %s, app: %s" % (aosp, app)

    @staticmethod
    def set_favorites():
        print "setting all favorite coworkers...",
        contacts_view.set_all_favorites()
        print "Done"

    @staticmethod
    def usb_enable():
        print "Enabling USB via spud port...",
        usb_enable()
        print "Done"

    def reboot(self):
        print "rebooting...",
        ss = SpudSerial(cfg.site['SerialDev'])
        self.parent.log_action(ss, {'cmd': 'cd\n', 'new_cwd': 'data'})
        self.parent.log_action(ss, {'cmd': 'reboot\n', 'new_cwd': '', 'expect': 'mtp_open', 'dead_air_timeout': 20,
                                    'timeout': 120})
        print "Done"

    def create_softphone_frames(self):
        acct_specs = []
        for username in [cfg.site['DefaultSoftphoneUser'], cfg.site['DefaultForwardAccount']]:
            softphone = get_softphone(username)
            softphone.set_incoming_response(180)
            acct_specs.append({'label': username, 'softphone': softphone})
        self.parent.softphone_frame = create_softphone_frame(self, acct_specs)

    def get_screenshot_adb_and_rotate(self):
        self.parent.__class__.get_screenshot_adb()
        self.parent.rotate_image(redraw_cwin=False)


# inspector.py instantiates the Inspector class, then calls install(), passing the Inspector instance as an argument
def install(parent):

    # - install drop-down menu items appropriate for ePhone7
    # - "cmd_types" key values are the labels for drop-down menus in Inspector
    # - new commands listed in "cmd_types[key]" are added to the menu labeled with that key
    # - if there is no drop-down menu labeled with a key, a new drop-down menu will be created

    e7_cmds = E7Commands(parent)
    cmd_types = {
        'Appium Actions': [
            {'label': 'Dial Advanced Settings Code', 'command': e7_cmds.dial_advanced_settings},
            {'label': 'Dial Alpha OTA Code', 'command': e7_cmds.dial_alpha_ota},
            {'label': 'Dial Beta OTA Code', 'command': e7_cmds.dial_beta_ota},
            {'label': 'Dial Current OTA Code', 'command': e7_cmds.dial_show_ota},
            {'label': 'Dial Production OTA Code', 'command': e7_cmds.dial_prod_ota},
            {'label': 'Set Coworker Favorites', 'command': e7_cmds.set_favorites}
        ],
        'Other Actions': [
            {'label': 'Enable USB', 'command': e7_cmds.usb_enable},
            {'label': 'Create Softphones', 'command': e7_cmds.create_softphone_frames},
            {'label': 'Reboot', 'command': e7_cmds.reboot}
        ]
    }
    for cmd_type in cmd_types:
        if cmd_type not in parent.menu.submenus:
            parent.menu.add_submenu(cmd_type)
        for cmd_spec in cmd_types[cmd_type]:
            parent.menu.submenus[cmd_type].add_command(label=cmd_spec['label'], command=cmd_spec['command'])

    # add locator type options for various ePhone7 views
    parent.locator_by_values += ('contacts_locator', 'voicemail_locator', 'history_locator',
                                 'dial_locator', 'prefs_locator', 'contacts_locator_all',
                                 'voicemail_locator_all', 'history_locator_all', 'dial_locator_all',
                                 'prefs_locator_all')
    parent.update_locator_list()
    parent.views = {'contacts': contacts_view, 'history': history_view, 'voicemail': voicemail_view, 'dial': dial_view,
                    'prefs': prefs_view}
    parent.get_screenshot_adb = e7_cmds.get_screenshot_adb_and_rotate


