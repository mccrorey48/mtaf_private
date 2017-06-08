import os
import sys
from Tkinter import Tk, Frame, Button, Text, NORMAL, DISABLED, Scrollbar, Entry, StringVar, IntVar, HORIZONTAL
from ttk import Combobox
from time import sleep

from pyand import ADB
from selenium.common.exceptions import WebDriverException
import lib.logging_esi as logging
from ePhone7.config.configure import cfg
from ePhone7.utils.spud_serial import SpudSerial
from ePhone7.utils.usb_enable import usb_enable
from ePhone7.views import *
from lib.user_exception import UserException as Ux
from ePhone7.utils.versions import *
from lib.android import expand_zpath
from ePhone7.utils.versions import force_aosp_downgrade, remove_apk_upgrades

log = logging.get_logger('esi.appium_gui')


class Command(object):
    def __init__(self, text, name, require_appium=True):
        self.text = text
        self.name = name
        self.require_appium = require_appium

commands = []
commands.append(Command("Start Appium", "start_appium", require_appium=False))
commands.append(Command("Stop Appium", "stop_appium", require_appium=True))
commands.append(Command("Restart Appium", "restart_appium"))
commands.append(Command("Install APK 1.0.10", "install_apk_1_0_10", require_appium=False))
commands.append(Command("Install APK 1.3.6", "install_apk_1_3_6", require_appium=False))
commands.append(Command("Get Current Activity", "get_current_activity"))
commands.append(Command("Startup", "startup"))
commands.append(Command("Log In", "login"))
commands.append(Command("Accept T&C", "accept_tnc"))
commands.append(Command("Skip Walkthrough", "skip_walkthrough"))
commands.append(Command("Log Out", "logout"))
commands.append(Command("Enable USB", "usb_enable", require_appium=False))
commands.append(Command("Set Alpha OTA Server", "set_alpha_ota_server"))
commands.append(Command("Reboot", "reboot", require_appium=False))
commands.append(Command("Get Installed Versions", "get_installed_versions", require_appium=False))
commands.append(Command("Get Alpha Current Versions", "get_alpha_current_versions", require_appium=False))
commands.append(Command("Get Beta Current Versions", "get_beta_current_versions", require_appium=False))
commands.append(Command("Get Production Current Versions", "get_prod_current_versions", require_appium=False))
commands.append(Command("Remove APK Upgrades", "remove_apk_upgrades", require_appium=False))
commands.append(Command("Get All Coworker Contacts", "get_all_coworker_contacts", require_appium=True))
commands.append(Command("Dial Advanced Settings Code", "dial_advanced_settings", require_appium=True))
commands.append(Command("Dial Alpha OTA Code", "dial_alpha_ota", require_appium=True))
commands.append(Command("Dial Beta OTA Code", "dial_beta_ota", require_appium=True))
commands.append(Command("Dial Prod OTA Code", "dial_prod_ota", require_appium=True))
commands.append(Command("Dial Current OTA Code", "dial_show_ota", require_appium=True))
commands.append(Command("Toggle Multi-Edit", "toggle_multi_edit", require_appium=True))
commands.append(Command("Force AOSP Downgrade", "force_aosp_downgrade", require_appium=False))


class ScrolledLogwin(Text):
    def __init__(self, parent, **kwargs):
        Text.__init__(self, parent, **kwargs)
        self.scrollback = 5000
        self.configure(state=DISABLED)
        self.sb = Scrollbar(self.master, command=self.yview)
        self["yscrollcommand"] = self.sb.set
        # self.hsb = Scrollbar(self.master, command=self.xview, orient=HORIZONTAL)
        # self["xscrollcommand"] = self.hsb.set
        self.sb.grid(row=0, column=1, sticky='ns', padx=2, pady=2)
        # self.hsb.grid(row=1, column=0, sticky='ew')
        self.print_buf = ''

    def write(self, _txt):
        if _txt[-1] == '\n':
            eol = True
        else:
            eol = False
        lines = _txt.strip().split('\n')
        self.configure(state=NORMAL)
        for line in lines[:-1]:
            self.insert('end', line + '\n')
        if len(lines):
            self.insert('end', lines[-1])
        if eol:
            self.insert('end', '\n')
        self.delete('0.0', 'end - %d lines' % self.scrollback)
        self.see('end')
        self.configure(state=DISABLED)
        self.update_idletasks()


class LogFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg='gray')
        print "parent = " + repr(parent)
        self.txt = ScrolledLogwin(self, width=80, height=10, name='cmd')
        self.txt.grid(row=0, column=0, sticky='news', padx=2, pady=2)

    def write(self, *args, **kwargs):
        self.txt.write(*args, **kwargs)

    def flush(self, *args, **kwargs):
        pass


class TestGui(Frame):

    elems = []
    appium_is_open = False
    appium_btns = []
    noappium_btns = []
    elem_indices = []

    def __init__(self, parent):
        Frame.__init__(self, parent, bg="tan")
        self.btn_frame = Frame(self, bg="cyan")
        row = None
        nrows = int(round(float(len(commands))/2))
        for row in range(nrows):
            cmd = commands[row * 2]
            btn = Button(self.btn_frame, text=cmd.text, command=lambda name=cmd.name: self.do_cmd(name), state=DISABLED)
            if cmd.require_appium:
                self.appium_btns.append(btn)
            else:
                self.noappium_btns.append(btn)
            # print "button %s at row %s" % (cmd.text, row)
            btn.grid(row=row, column=0, sticky='w', padx=2, pady=2)
            if len(commands) > (row * 2) + 1:
                cmd = commands[(row * 2) + 1]
                btn = Button(self.btn_frame, text=cmd.text, command=lambda name=cmd.name: self.do_cmd(name), state=DISABLED)
                if cmd.require_appium:
                    self.appium_btns.append(btn)
                else:
                    self.noappium_btns.append(btn)
                # print "button %s at row %s" % (cmd.text, row)
                btn.grid(row=row, column=0, sticky='e', padx=2, pady=2)

        self.find_frame = Frame(self.btn_frame, bg='brown')
        btn = Button(self.find_frame, text="find elements:", command=self.find_elements, state=DISABLED)
        self.appium_btns.append(btn)
        self.find_by_var = StringVar()
        self.find_by_var.set('zpath')
        self.find_frame.by = Combobox(self.find_frame, width=6, values=['zpath', 'xpath', 'id'], textvariable=self.find_by_var)
        self.find_frame.by.grid(row=0, column=1, padx=2, pady=2, sticky='ew')
        self.find_value_var = StringVar()
        self.find_frame.value = Entry(self.find_frame, width=60, textvariable=self.find_value_var)
        self.find_frame.hsb = Scrollbar(self.find_frame, orient=HORIZONTAL, command=self.find_frame.value.xview)
        self.find_frame.value["xscrollcommand"] = self.find_frame.hsb.set
        btn.grid(row=0, column=0, padx=2, pady=2)
        self.find_frame.grid_columnconfigure(1, weight=1)
        self.find_frame.value.grid(row=0, column=2, padx=2, pady=2, sticky='ew')
        self.find_frame.hsb.grid(row=1, column=2, sticky='ew')
        row += 1
        self.find_frame.grid(row=row, column=0, sticky='ew', padx=2, pady=2)

        self.keycode_frame = Frame(self.btn_frame, bg='brown')
        btn = Button(self.keycode_frame, text="send keycode:", command=self.send_keycode, state=DISABLED)
        self.appium_btns.append(btn)
        self.keycode = IntVar()
        self.keycode.set(4)
        self.keycode_frame.value = Entry(self.keycode_frame, width=10, textvariable=self.keycode)
        btn.grid(row=0, column=0, padx=2, pady=2, sticky='w')
        self.keycode_frame.grid_columnconfigure(1, weight=1)
        self.keycode_frame.value.grid(row=0, column=1, padx=2, pady=2, sticky='w')
        row += 1
        self.keycode_frame.grid(row=row, column=0, sticky='ew', padx=2, pady=2)

        self.attr_frame = Frame(self.btn_frame, bg='brown')
        btn = Button(self.attr_frame, text="get element attributes:", command=self.get_elem_attrs, state=DISABLED)
        self.appium_btns.append(btn)
        btn.grid(row=0, column=0, padx=2, pady=2)
        btn = Button(self.attr_frame, text="get element color:", command=self.get_elem_color, state=DISABLED)
        self.appium_btns.append(btn)
        btn.grid(row=0, column=1, padx=2, pady=2)
        self.elem_index = StringVar()
        self.elem_index.set('')
        self.attr_frame.index = Combobox(self.attr_frame, width=6, values=[], textvariable=self.elem_index)
        self.attr_frame.index.grid(row=0, column=2, padx=2, pady=2, sticky='ew')
        row += 1
        self.attr_frame.grid(row=row, column=0, sticky='ew', padx=2, pady=2)

        self.btn_frame.grid_columnconfigure(0, weight=1)
        self.btn_frame.grid(row=0, column=0, sticky='ew', padx=2, pady=2)
        self.logframe = LogFrame(self)
        sys.stdout = self.logframe
        self.logframe.grid_columnconfigure(0, weight=1)
        self.logframe.grid_rowconfigure(0, weight=1)
        self.logframe.grid(row=1, column=0, padx=2, pady=2, sticky='news')
        self.bottom_frame = Frame(self, bg="cyan")
        self.bottom_frame.grid_columnconfigure(0, weight=1)
        self.bottom_frame.Quit = Button(self.bottom_frame, text="Quit", command=self.close_appium_and_quit)
        self.bottom_frame.Quit.grid(row=0, column=0, sticky='e', padx=2, pady=2)
        self.bottom_frame.grid(row=2, column=0, padx=2, pady=2, sticky='news')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid(row=0, column=0, padx=2, pady=2, sticky='nsew')
        for btn in self.appium_btns:
            btn.configure(state=DISABLED)
        for btn in self.noappium_btns:
            btn.configure(state=NORMAL)

    def close_appium_and_quit(self):
        if self.appium_is_open:
            self.close_appium()
        root.destroy()

    def send_keycode(self):
        base_view.driver.keyevent(self.keycode.get())

    def find_elements(self):
        by = self.find_by_var.get()
        value = self.find_value_var.get()
        if by == 'zpath':
            value = expand_zpath(value)
            by = 'xpath'
            print "xpath = %s" % value
        self.elems = base_view.driver.find_elements(by, value)
        print "%s elements found" % len(self.elems)
        elem_indices = [str(i) for i in range(len(self.elems))]
        self.attr_frame.index.configure(values=elem_indices)
        if len(elem_indices):
            self.elem_index.set('0')
        else:
            self.elem_index.set('')

    def get_elem_attrs(self):
        text_index = self.elem_index.get()
        if text_index == '':
            return
        index = int(text_index)
        elem = self.elems[index]
        text = elem.text
        loc = elem.location
        size = elem.size
        x1 = int(loc['x'])
        y1 = int(loc['y'])
        w = int(size['width'])
        h = int(size['height'])
        x2 = x1 + w
        y2 = y1 + h
        print 'text: "%s", ul: (%d, %d), lr: (%d, %d), width: %d, height: %d' % (text, x1, y1, x2, y2, w, h)

    def get_elem_color(self):
        text_index = self.elem_index.get()
        if text_index == '':
            return
        index = int(text_index)
        elem = self.elems[index]
        base_view.get_screenshot_as_png('appium_gui', cfg.test_screenshot_folder)
        color = base_view.get_element_color_and_count('appium_gui', elem)
        print "color and count: %s" % color
        for color_name in ['favorite_on_color', 'favorite_off_color']:
            if base_view.color_match(color, cfg.colors['ContactsView'][color_name]):
                print color_name

    def open_appium(self, max_attempts=10, retry_seconds=5):
        attempts = 0
        while attempts < max_attempts:
            try:
                if attempts > 0:
                    print "\n(retrying) Opening Appium...",
                else:
                    print "Opening Appium...",
                self.update_idletasks()
                base_view.open_appium()
                break
            except Ux as e:
                print "UserException in open_appium: %s" % e.msg
                print "retrying:",
                sleep(retry_seconds)
        else:
            raise Ux("max attempts reached in open_appium")
        self.appium_is_open = True
        print "Done"
        for btn in self.appium_btns:
            btn.configure(state=NORMAL)
        for btn in self.noappium_btns:
            btn.configure(state=DISABLED)

    def close_appium(self):
        print "Closing Appium...",
        base_view.close_appium()
        self.appium_is_open = False
        print "Done"
        for btn in self.appium_btns:
            btn.configure(state=DISABLED)
        for btn in self.noappium_btns:
            btn.configure(state=NORMAL)

    @staticmethod
    def log_action(spud_serial, action):
        (reply, elapsed, groups) = spud_serial.do_action(action)
        lines = reply.split('\n')
        log.debug('cmd: %s\nelapsed: [%5.3f s]  \necho: "%s"\n' % (action['cmd'], elapsed, lines[0].encode('string_escape')))
        for line in lines[1:]:
            log.debug(' '*7 + line.encode('string_escape'))

    def reboot(self):
        ss = SpudSerial('/dev/ttyUSB0')
        self.log_action(ss, {'cmd': 'cd\n', 'new_cwd': 'data'})
        self.log_action(ss, {'cmd': 'reboot\n', 'new_cwd': '', 'expect': 'Restarting system', 'timeout': 1})
        self.log_action(ss, {'cmd': '', 'new_cwd': '', 'expect': 'mtp_open', 'timeout': 120})
        # while True:
        #     try:
        #         activity = base_view.driver.current_activity
        #         if activity is None:
        #             pass
        #         print activity
        #         sleep(1)
        #     except WebDriverException as e:
        #         print "got WebDriverException: %s" % e
        #         self.close_appium()
        #         break

    def do_cmd(self, name):
        if name == 'get_current_activity':
            print "current activity: " + base_view.driver.current_activity
        else:
            if name == 'login':
                print "logging in"
                login_view.login()
            elif name == 'start_appium':
                self.open_appium()
            elif name == 'stop_appium':
                self.close_appium()
            elif name == 'restart_appium':
                self.close_appium()
                self.open_appium()
            elif name == 'usb_enable':
                print "Enabling USB via spud port...",
                usb_enable()
                print "Done"
            elif name == 'accept_tnc':
                print "accepting terms and conditions...",
                tnc_view.accept_tnc()
                print "Done"
            elif name == 'startup':
                print "running startup...",
                base_view.startup()
                print "Done"
            elif name == 'set_alpha_ota_server':
                print "Setting alpha OTA server...",
                user_view.goto_tab('Dial')
                user_view.set_ota_server('alpha')
                print "Done"
            elif name == 'install_apk_1_0_10':
                print "Installing APK 1.0.10 using adb...",
                self.install_apk('1.0.10')
                print "Done"
            elif name == 'install_apk_1_3_6':
                print "Installing APK 1.3.6 using adb...",
                self.install_apk('1.3.6')
                print "Done"
            elif name == 'skip_walkthrough':
                print "skipping walkthrough"
                app_intro_view.skip_intro()
            elif name == 'reboot':
                print "rebooting...",
                self.reboot()
                print "Done"
            elif name == 'get_installed_versions':
                print "getting installed versions"
                aosp, app = get_installed_versions()
                print "aosp: %s, app: %s" % (aosp, app)
            elif name == 'get_alpha_current_versions':
                print "getting current alpha versions"
                aosp, app = get_current_versions('alpha')
                print "aosp: %s, app: %s" % (aosp, app)
            elif name == 'get_beta_current_versions':
                print "getting current beta versions"
                aosp, app = get_current_versions('beta')
                print "aosp: %s, app: %s" % (aosp, app)
            elif name == 'get_prod_current_versions':
                print "getting current prod versions"
                aosp, app = get_current_versions('prod')
                print "aosp: %s, app: %s" % (aosp, app)
            elif name == 'get_all_coworker_contacts':
                print "getting coworker contacts"
                contacts_group = cfg.site['Users']['R2d2User']['CoworkerContacts']
                nums = contacts_view.get_all_group_contacts(contacts_group)
                print repr(nums)
            elif name == 'dial_advanced_settings':
                print "dialing advanced settings code...",
                dial_view.dial_advanced_settings()
                dial_view.touch_call_button()
                print "Done"
            elif name == 'dial_alpha_ota':
                print "dialing alpha OTA code...",
                dial_view.dial_set_alpha_ota_server()
                dial_view.touch_call_button()
                print "Done"
            elif name == 'dial_beta_ota':
                print "dialing beta OTA code...",
                dial_view.dial_set_beta_ota_server()
                dial_view.touch_call_button()
                print "Done"
            elif name == 'dial_prod_ota':
                print "dialing prod OTA code...",
                dial_view.dial_set_production_ota_server()
                dial_view.touch_call_button()
                print "Done"
            elif name == 'dial_show_ota':
                print "dialing show OTA code...",
                dial_view.dial_show_ota_server()
                dial_view.touch_call_button()
                print "Done"
            elif name == 'toggle_multi_edit':
                print "Toggling Multi-Edit...",
                contacts_view.toggle_multi_edit()
                print "Done"
            elif name == 'force_aosp_downgrade':
                print "Forcing AOSP Downgrade...",
                force_aosp_downgrade('2.3.8')
                print "Done"
            else:
                raise Ux('command %s not defined' % name)
            if self.appium_is_open:
                print "current activity: " + base_view.driver.current_activity

    @staticmethod
    def install_apk(version):
        adb = ADB()
        apk_path = os.path.join(cfg.site["ApksHome"], "%s.apk" % version)
        print "Installing " + apk_path
        output = adb.run_cmd("install -r -d %s" % apk_path)
        for line in output.split('\n'):
            log.debug(line.encode('string_escape'))

    def __del__(self):
        print "Closing Appium...",
        self.update_idletasks()
        self.after(500, base_view.close_appium)
        sleep(1)


root = Tk()
root.wm_title("Appium test utility")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
_app = TestGui(root)


def on_closing():
    if _app.appium_is_open:
        print "trying to close appium"
        _app.close_appium()
    sleep(5)
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
_app.mainloop()

# base_view.startup()
# login()
# for i in range(3):
#     # reboot()
    # base_view.startup()
# for i in range(10000):
#     try:
#         print "%s: current activity: %s" % (i, base_view.driver.current_activity)
#     except WebDriverException:
#         print "%s: got WebDriverException" % i
#     sleep(1)
# base_view.close_appium()

