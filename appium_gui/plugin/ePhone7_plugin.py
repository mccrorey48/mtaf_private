from ePhone7.views import *
from ePhone7.utils.usb_enable import usb_enable
from ePhone7.utils.versions import get_installed_versions
from ePhone7.config.configure import cfg
from ePhone7.utils.spud_serial import SpudSerial
from ePhone7.utils.get_softphone import get_softphone
from lib.user_exception import UserException as Ux
from Tkinter import Frame, IntVar, StringVar, Button, Checkbutton, Label, DISABLED, NORMAL


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

    def create_softphone_frame(self):
        self.parent.softphone_frame = Frame(self.parent, bg='brown')
        self.parent.softphone_frame.columnconfigure(0, weight=1)
        self.parent.top_frames.insert(1, self.parent.softphone_frame)
        self.parent.populate_top_frames()
        self.parent.softphone_frame.account1_frame = AccountFrame(self.parent.softphone_frame,
                                                                  cfg.site['DefaultSoftphoneUser'])
        self.parent.softphone_frame.account1_frame.grid(row=0, column=0, sticky='ew', padx=2, pady=2)
        self.parent.softphone_frame.account2_frame = AccountFrame(self.parent.softphone_frame,
                                                                  cfg.site['DefaultForwardAccount'])
        self.parent.softphone_frame.account2_frame.grid(row=1, column=0, sticky='ew', padx=2, pady=2)
        label_position = 1
        last_label = None
        submenu = self.parent.menu.submenus['Other Actions']
        while True:
            current_label = submenu.entrycget(label_position, 'label')
            if current_label == last_label:
                raise Ux('attempting to disable Create Softphones menu item, label not found')
            if current_label == 'Create Softphones':
                submenu.entryconfigure(label_position, state=DISABLED)
                break
            last_label = current_label
            label_position += 1


class AccountFrame(Frame):
    def __init__(self, parent, user_name, *args, **kwargs):
        Frame.__init__(self, parent, bg='tan', *args, **kwargs)
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

        self.softphone = get_softphone(user_name)
        self.softphone.set_incoming_response(180)
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


# appium_gui.py instantiates the AppiumGui class, then calls install(), passing the AppiumGui instance as an argument
def install(parent):

    # - install drop-down menu items appropriate for ePhone7
    # - "cmd_types" key values are the labels for drop-down menus in AppiumGui
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
            {'label': 'Create Softphones', 'command': e7_cmds.create_softphone_frame},
            {'label': 'Reboot', 'command': e7_cmds.reboot}
        ]
    }
    for cmd_type in cmd_types:
        if cmd_type not in parent.menu.submenus:
            parent.menu.add_submenu(cmd_type)
        for cmd_spec in cmd_types[cmd_type]:
            parent.menu.submenus[cmd_type].add_command(label=cmd_spec['label'], command=cmd_spec['command'])

    # add locator type options for variouis ePhone7 views
    values = parent.btn_frame.find_frame.by.cget('values')
    values += ('contacts_locator', 'voicemail_locator', 'history_locator',
               'dial_locator', 'prefs_locator', 'contacts_locator_all',
               'voicemail_locator_all', 'history_locator_all', 'dial_locator_all',
               'prefs_locator_all')
    parent.btn_frame.find_frame.by.configure(values=values)


