from ePhone7.views import *
from ePhone7.lib.utils.usb_enable import usb_enable
from ePhone7.lib.utils.versions import get_installed_versions
from ePhone7.config.configure import cfg
from ePhone7.lib.utils.spud_serial import SpudSerial
from ePhone7.lib.utils.get_softphone import get_softphone
import six
from mtaf.user_exception import UserException as Ux
import os
if six.PY3:
    from tkinter import *
else:
    from Tkinter import Frame, IntVar, StringVar, Label, Checkbutton, Button
    from Tkconstants import DISABLED, NORMAL


class AccountFrame(Frame):
    def __init__(self, parent, user_name, softphone, *args, **kwargs):
        Frame.__init__(self, parent, bg='tan', *args, **kwargs)
        self.softphone = softphone
        self.softphone.set_incoming_response(180)
        self.registered_var = IntVar()
        self.registered_var.set(0)
        self.old_reg_status = None
        self.status_var = StringVar()
        self.status_var.set('None')
        self.remote_var = StringVar()
        self.remote_var.set('')

        self.label = Label(self, text=user_name)
        self.label.grid(row=0, column=0, sticky='w', padx=2, pady=2, ipady=3)

        self.cb = Checkbutton(self, text='Registered', variable=self.registered_var)
        self.cb.grid(row=0, column=1, padx=2, ipady=1)

        self.status = Frame(self)
        self.status.label = Label(self.status, text='Status: ')
        self.status.label.grid(row=0, column=0, padx=2, ipady=2)
        self.status.value = Label(self.status, textvariable=self.status_var, width=10)
        self.status.value.grid(row=0, column=1, padx=2, ipady=2)
        self.status.grid(row=0, column=2, padx=5, pady=2)

        self.answer = Button(self, text='Answer', command=lambda: self.softphone.send_response_code(200),
                             state=DISABLED)
        self.answer.grid(row=0, column=3, padx=5, pady=2)

        self.hangup = Button(self, text='Hang Up', command=lambda: self.softphone.end_call(), state=DISABLED)
        self.hangup.grid(row=0, column=4, padx=5, pady=2)

        self.remote = Label(self, textvariable=self.remote_var, width=10)
        self.remote.grid(row=0, column=5, padx=5, pady=2, ipady=3, sticky='ew')
        self.columnconfigure(5, weight=1)

        self.after(100, self.check_status)

    def check_status(self):
        info = self.softphone.account_info.account.info()
        if self.old_reg_status != info.reg_status:
            self.registered_var.set(info.reg_status == 200)
            print "%s reg status changed from %s to %s" % (info.uri, self.old_reg_status, info.reg_status)
            self.old_reg_status = info.reg_status
        old_call_status = self.status_var.get()
        new_call_status = self.softphone.account_info.call_status
        remote_uri = self.softphone.account_info.remote_uri
        if new_call_status != old_call_status:
            self.status_var.set(new_call_status)
            if remote_uri is None:
                self.remote_var.set('')
            else:
                self.remote_var.set('--> ' + self.softphone.account_info.remote_uri)
            # if remote_uri is None:
            #     print "%s: %5s --> %5s" % (self.softphone.uri, old_call_status, new_call_status)
            # else:
            #     print "%s: %5s --> %5s  [remote: %s]" % (self.softphone.uri, old_call_status, new_call_status,
            #                                              remote_uri)
            if new_call_status == 'call':
                self.hangup.configure(state=NORMAL)
            else:
                self.hangup.configure(state=DISABLED)
            if new_call_status == 'early':
                self.answer.configure(state=NORMAL)
            else:
                self.answer.configure(state=DISABLED)
        self.after(100, self.check_status)


class E7Commands(object):

    def __init__(self, app):
        self.app = app

    @staticmethod
    def dial_beta_ota():
        six.print_("dialing beta OTA code...",)
        user_view.goto_tab('Dial')
        user_view.touch_element_with_text('Dial')
        dial_view.dial_set_beta_ota_server()
        dial_view.touch_call_button()
        six.print_("Done")

    @staticmethod
    def dial_alpha_ota():
        six.print_("dialing alpha OTA code...",)
        user_view.goto_tab('Dial')
        user_view.touch_element_with_text('Dial')
        dial_view.dial_set_alpha_ota_server()
        dial_view.touch_call_button()
        six.print_("Done")

    @staticmethod
    def dial_prod_ota():
        six.print_("dialing prod OTA code...",)
        user_view.goto_tab('Dial')
        dial_view.dial_set_production_ota_server()
        dial_view.touch_call_button()
        six.print_("Done")

    @staticmethod
    def dial_show_ota():
        six.print_("dialing show OTA code...",)
        user_view.goto_tab('Dial')
        dial_view.dial_show_ota_server()
        dial_view.touch_call_button()
        six.print_("Done")

    @staticmethod
    def dial_advanced_settings():
        six.print_("dialing advanced settings code...",)
        user_view.goto_tab('Dial')
        dial_view.dial_advanced_settings()
        dial_view.touch_call_button()
        six.print_("Done")

    @staticmethod
    def get_installed_versions():
        six.print_("getting installed versions")
        # self.update_idletasks()
        aosp, app = get_installed_versions()
        six.print_("aosp: %s, app: %s" % (aosp, app))

    @staticmethod
    def set_favorites():
        six.print_("setting all favorite coworkers...",)
        contacts_view.set_all_favorites()
        six.print_("Done")

    @staticmethod
    def usb_enable():
        six.print_("Enabling USB via spud port...",)
        usb_enable()
        six.print_("Done")

    def reboot(self):
        six.print_("rebooting...",)
        ss = SpudSerial(cfg.site['SerialDev'])
        self.app.log_action(ss, {'cmd': 'cd\n', 'new_cwd': 'data'})
        self.app.log_action(ss, {'cmd': 'reboot\n', 'new_cwd': '', 'expect': 'mtp_open', 'dead_air_timeout': 20,
                                 'timeout': 120})
        six.print_("Done")

    def create_softphone_frame(self, acct_specs):
        frame = Frame(self.app, bg='brown')
        frame.columnconfigure(0, weight=1)
        for row, acct_spec in enumerate(acct_specs):
            frame.account1_frame = AccountFrame(frame, acct_spec['label'], acct_spec['softphone'])
            frame.account1_frame.grid(row=row, column=0, sticky='ew', padx=2, pady=2)
        self.app.top_frames.insert(1, frame)
        self.app.populate_top_frames()

    def create_softphone_frames(self):
        acct_specs = []
        for username in [cfg.site['DefaultSoftphoneUser'], cfg.site['DefaultForwardAccount']]:
            softphone = get_softphone(username, wav_dir=os.path.join(self.app.cfg['tmp_dir'], 'wav'),
                                      require_reg_ok=False)
            softphone.set_incoming_response(180)
            acct_specs.append({'label': username, 'softphone': softphone})
        self.create_softphone_frame(acct_specs)

    def get_screenshot_adb_and_rotate(self):
        self.app.get_screenshot_adb()
        six.print_("-->rotating image...")
        self.app.rotate_image()
        six.print_("Done")


class Plugin(object):

    def install_plugin(self, app):

        # - install drop-down menu items appropriate for ePhone7
        # - "cmd_types" key values are the labels for drop-down menus in Inspector
        # - new commands listed in "cmd_types[key]" are added to the menu labeled with that key
        # - if there is no drop-down menu labeled with a key, a new drop-down menu will be created

        e7_cmds = E7Commands(app)
        app.user_cmds.update({
            'Dial Advanced Settings Code': e7_cmds.dial_advanced_settings,
            'Dial Alpha OTA Code': e7_cmds.dial_alpha_ota,
            'Dial Beta OTA Code': e7_cmds.dial_beta_ota,
            'Dial Current OTA Code': e7_cmds.dial_show_ota,
            'Dial Production OTA Code': e7_cmds.dial_prod_ota,
            'Set Coworker Favorites': e7_cmds.set_favorites,
            'Enable USB': e7_cmds.usb_enable,
            'Create Softphones': e7_cmds.create_softphone_frames,
            'Reboot': e7_cmds.reboot,
            'Get Screenshot ADB': e7_cmds.get_screenshot_adb_and_rotate
        })
        menu_items = {
            'Appium Actions': [
                {'label': 'Dial Advanced Settings Code', 'uses_appium': True},
                {'label': 'Dial Alpha OTA Code', 'uses_appium': True},
                {'label': 'Dial Beta OTA Code', 'uses_appium': True},
                {'label': 'Dial Current OTA Code', 'uses_appium': True},
                {'label': 'Dial Production OTA Code', 'uses_appium': True},
                {'label': 'Set Coworker Favorites', 'uses_appium': True}
            ],
            'Other Actions': [
                {'label': 'Enable USB', 'uses_appium': True},
                {'label': 'Create Softphones', 'uses_appium': None},
                {'label': 'Reboot', 'uses_appium': True}
            ]
        }
        for menu_label in menu_items:
            app.menu.add_submenu(menu_label, app.make_menu_items(menu_items[menu_label]))
        app.menu.enable_items(app.appium_is_open)

        # add locator type options for various ePhone7 views
        app.locator_by_values += ('contacts_locator', 'voicemail_locator', 'history_locator',
                                  'dial_locator', 'prefs_locator', 'contacts_locator_all',
                                  'voicemail_locator_all', 'history_locator_all', 'dial_locator_all',
                                  'prefs_locator_all')
        app.update_locator_list()
        app.views = {'contacts': contacts_view, 'history': history_view, 'voicemail': voicemail_view, 'dial': dial_view,
                     'prefs': prefs_view}


