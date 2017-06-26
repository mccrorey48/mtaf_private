import os
import sys
from Tkinter import *
from ttk import Combobox
from time import sleep

from pyand import ADB
import lib.logging_esi as logging
from ePhone7.config.configure import cfg
from ePhone7.utils.spud_serial import SpudSerial
from ePhone7.utils.get_softphone import get_softphone
from ePhone7.utils.usb_enable import usb_enable
from ePhone7.views import *
from lib.user_exception import UserException as Ux
from ePhone7.utils.versions import *
from lib.android import expand_zpath
from ePhone7.utils.versions import force_aosp_downgrade, remove_apk_upgrades
from ePhone7.utils.csv.xml_to_csv import xml_folder_to_csv

log = logging.get_logger('esi.appium_gui')


class Command(object):
    def __init__(self, label, action):
        self.label = label
        self.action = action

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
        Frame.__init__(self, parent, bg='brown')
        print "parent = " + repr(parent)
        self.txt = ScrolledLogwin(self, width=80, height=10, name='cmd')
        self.txt.grid(row=0, column=0, sticky='news', padx=2, pady=2)

    def write(self, *args, **kwargs):
        self.txt.write(*args, **kwargs)

    def flush(self, *args, **kwargs):
        pass

class AccountFrame(Frame):
    def __init__(self, parent, user_name, *args, **kwargs):
        Frame.__init__(self, parent, bg='tan', *args, **kwargs)
        self.registered_var = IntVar()
        self.registered_var.set(0)
        self.status_var = StringVar()
        self.status_var.set('')
        self.label = Label(self, text=user_name)
        self.label.grid(row=0, column=0, sticky='w', padx=2, pady=2)
        self.cb = Checkbutton(self, text='Registered', variable=self.registered_var)
        self.cb.grid(row=0, column=1, padx=2)
        self.status = Frame(self)
        self.status.label = Label(self.status, text='Status: ')
        self.status.label.grid(row=0, column=0)
        self.status.value = Label(self.status, textvariable=self.status_var, width=10)
        self.status.value.grid(row=0, column=1)
        self.status.grid(row=0, column=2, padx=5, pady=2)
        self.answer = Button(self, text='Answer', command=lambda: self.softphone.send_response_code(200), state=DISABLED)
        self.answer.grid(row=0, column=3, padx=5, pady=2)
        self.hangup = Button(self, text='Hang Up', command=lambda: self.softphone.end_call(), state=DISABLED)
        self.hangup.grid(row=0, column=4, padx=5, pady=2)
        self.softphone = get_softphone(user_name)
        self.softphone.set_incoming_response(180)
        self.after(100, self.check_status)

    def check_status(self):
        self.registered_var.set(self.softphone.account_info.account.info().reg_status == 200)
        old_call_status = self.status_var.get()
        new_call_status = self.softphone.account_info.call_status
        if new_call_status != old_call_status:
            self.status_var.set(new_call_status)
            print "call status = " + new_call_status
            if new_call_status == 'call':
                self.hangup.configure(state=NORMAL)
            else:
                self.hangup.configure(state=DISABLED)
            if new_call_status == 'early':
                self.answer.configure(state=NORMAL)
            else:
                self.answer.configure(state=DISABLED)
        self.after(100, self.check_status)


class TestGui(Frame):

    elems = []
    appium_is_open = False
    appium_btns = []
    noappium_btns = []
    elem_indices = []
    appium_commands = []
    other_commands = []

    def __init__(self, parent):
        Frame.__init__(self, parent, bg="brown")
        self.create_commands()
        self.create_menus(parent)
        self.top_frame_row = 0
        self.btn_frame = None
        self.create_btn_frame()
        self.softphone_frame = None
        self.create_softphone_frame()
        self.create_logframe()
        self.create_bottom_frame()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid(row=0, column=0, padx=2, pady=2, sticky='nsew')
        for btn in self.appium_btns:
            btn.configure(state=DISABLED)
        for i in range(self.appium_sub_menu_max_index):
            self.appium_sub_menu.entryconfig(i + 1, state=DISABLED)
        for btn in self.noappium_btns:
            btn.configure(state=NORMAL)
        for i in range(self.other_sub_menu_max_index):
            self.other_sub_menu.entryconfig(i + 1, state=NORMAL)

    def create_bottom_frame(self):
        self.bottom_frame = Frame(self, bg="tan")
        self.bottom_frame.grid_columnconfigure(0, weight=1)
        self.bottom_frame.Quit = Button(self.bottom_frame, text="Quit", command=self.close_appium_and_quit)
        self.bottom_frame.Quit.grid(row=0, column=0, sticky='e', padx=2, pady=2)
        self.bottom_frame.grid(row=self.top_frame_row, column=0, padx=2, pady=2, sticky='news')

    def create_logframe(self):
        self.logframe = LogFrame(self)
        sys.stdout = self.logframe
        self.logframe.grid_columnconfigure(0, weight=1)
        self.logframe.grid_rowconfigure(0, weight=1)
        self.logframe.grid(row=self.top_frame_row, column=0, padx=2, pady=2, sticky='news')
        self.top_frame_row += 1

    def create_softphone_frame(self):
        self.softphone_frame = Frame(self, bg='brown')
        self.softphone_frame.grid_columnconfigure(0, weight=1)
        self.softphone_frame.account1_frame = AccountFrame(self.softphone_frame, cfg.site['DefaultSoftphoneUser'])
        self.softphone_frame.account1_frame.grid(row=0, column=0, sticky='ew', padx=2, pady=2)
        self.softphone_frame.account2_frame = AccountFrame(self.softphone_frame, cfg.site['DefaultForwardAccount'])
        self.softphone_frame.account2_frame.grid(row=1, column=0, sticky='ew', padx=2, pady=2)
        self.softphone_frame.grid(row=self.top_frame_row, column=0, sticky='ew', padx=2, pady=2)
        self.top_frame_row += 1

    def create_btn_frame(self):
        btn_frame_row = 0
        self.btn_frame = Frame(self, bg="brown")
        self.btn_frame.find_frame = Frame(self.btn_frame, bg='tan')
        btn = Button(self.btn_frame.find_frame, text="find elements:", command=self.find_elements, state=DISABLED)
        self.appium_btns.append(btn)
        self.find_by_var = StringVar()
        self.find_by_var.set('zpath')
        self.btn_frame.find_frame.by = Combobox(self.btn_frame.find_frame, width=16,
                                                values=['zpath', 'xpath', 'id', '-android uiautomator'],
                                                textvariable=self.find_by_var)
        self.btn_frame.find_frame.by.grid(row=0, column=1, padx=2, pady=2, sticky='ew')
        self.find_value_var = StringVar()
        self.btn_frame.find_frame.value = Entry(self.btn_frame.find_frame, width=60, textvariable=self.find_value_var)
        self.btn_frame.find_frame.hsb = Scrollbar(self.btn_frame.find_frame, orient=HORIZONTAL,
                                                  command=self.btn_frame.find_frame.value.xview)
        self.btn_frame.find_frame.value["xscrollcommand"] = self.btn_frame.find_frame.hsb.set
        btn.grid(row=0, column=0, padx=2, pady=2)
        self.btn_frame.find_frame.grid_columnconfigure(1, weight=1)
        self.btn_frame.find_frame.value.grid(row=0, column=2, padx=2, pady=2, sticky='ew')
        self.btn_frame.find_frame.hsb.grid(row=1, column=2, sticky='ew')
        self.btn_frame.find_frame.grid(row=btn_frame_row, column=0, sticky='ew', padx=2, pady=2)
        btn_frame_row += 1
        self.btn_frame.keycode_frame = Frame(self.btn_frame, bg='tan')
        btn = Button(self.btn_frame.keycode_frame, text="send keycode:", command=self.send_keycode, state=DISABLED)
        self.appium_btns.append(btn)
        self.keycode = IntVar()
        self.keycode.set(4)
        self.btn_frame.keycode_frame.value = Entry(self.btn_frame.keycode_frame, width=10, textvariable=self.keycode)
        btn.grid(row=0, column=0, padx=2, pady=2, sticky='w')
        self.btn_frame.keycode_frame.grid_columnconfigure(1, weight=1)
        self.btn_frame.keycode_frame.value.grid(row=0, column=1, padx=2, pady=2, sticky='w')
        self.btn_frame.keycode_frame.grid(row=btn_frame_row, column=0, sticky='ew', padx=2, pady=2)
        btn_frame_row += 1
        self.btn_frame.attr_frame = Frame(self.btn_frame, bg='tan')
        btn = Button(self.btn_frame.attr_frame, text="get element attributes", command=self.get_elem_attrs,
                     state=DISABLED)
        self.appium_btns.append(btn)
        btn.grid(row=0, column=0, padx=2, pady=2)
        btn = Button(self.btn_frame.attr_frame, text="get element color", command=self.get_elem_color, state=DISABLED)
        self.appium_btns.append(btn)
        btn.grid(row=0, column=1, padx=2, pady=2)
        btn = Button(self.btn_frame.attr_frame, text="click element", command=self.click_element, state=DISABLED)
        self.appium_btns.append(btn)
        btn.grid(row=0, column=2, padx=2, pady=2)
        self.elem_index = StringVar()
        self.elem_index.set('')
        self.btn_frame.attr_frame.index = Combobox(self.btn_frame.attr_frame, width=6, values=[],
                                                   textvariable=self.elem_index)
        self.btn_frame.attr_frame.index.grid(row=0, column=3, padx=2, pady=2, sticky='ew')
        self.btn_frame.attr_frame.grid(row=btn_frame_row, column=0, sticky='ew', padx=2, pady=2)
        self.btn_frame.grid_columnconfigure(0, weight=1)
        self.btn_frame.grid(row=self.top_frame_row, column=0, sticky='ew', padx=2, pady=2)
        self.top_frame_row += 1

    def create_menus(self, parent):
        menu = Menu(parent)
        self.appium_sub_menu = Menu(menu)
        self.appium_sub_menu_max_index = 0
        menu.add_cascade(label="Appium Actions", menu=self.appium_sub_menu)
        self.other_sub_menu = Menu(menu)
        self.other_sub_menu_max_index = 0
        menu.add_cascade(label="Other Actions", menu=self.other_sub_menu)
        for command in self.appium_commands:
            self.appium_sub_menu.add_command(label=command.label, command=command.action)
            self.appium_sub_menu_max_index += 1
        for command in self.other_commands:
            self.other_sub_menu.add_command(label=command.label, command=command.action)
            self.other_sub_menu_max_index += 1
        parent.config(menu=menu)

    def create_commands(self):
        self.appium_commands.append(Command("Accept T&C", lambda: self.do_cmd(self.accept_tnc)))
        self.appium_commands.append(
            Command("Dial Advanced Settings Code", lambda: self.do_cmd(self.dial_advanced_settings)))
        self.appium_commands.append(Command("Dial Alpha OTA Code", lambda: self.do_cmd(self.dial_alpha_ota)))
        self.appium_commands.append(Command("Dial Beta OTA Code", lambda: self.do_cmd(self.dial_beta_ota)))
        self.appium_commands.append(Command("Dial Current OTA Code", lambda: self.do_cmd(self.dial_show_ota)))
        self.appium_commands.append(Command("Dial Prod OTA Code", lambda: self.do_cmd(self.dial_prod_ota)))
        self.appium_commands.append(
            Command("Get All Coworker Contacts", lambda: self.do_cmd(self.get_all_coworker_contacts)))
        self.appium_commands.append(Command("Get Current Activity", lambda: self.do_cmd(self.get_current_activity)))
        self.appium_commands.append(Command("Get Screenshot", lambda: self.do_cmd(self.get_screenshot)))
        self.appium_commands.append(Command("Get XML/CSV", lambda: self.do_cmd(self.get_xml)))
        self.appium_commands.append(Command("Log In", lambda: self.do_cmd(self.login)))
        self.appium_commands.append(Command("Restart Appium", lambda: self.do_cmd(self.restart_appium)))
        self.appium_commands.append(Command("Set Alpha OTA Server", lambda: self.do_cmd(self.set_alpha_ota_server)))
        self.appium_commands.append(Command("Skip Walkthrough", lambda: self.do_cmd(self.skip_walkthrough)))
        self.appium_commands.append(Command("Startup", lambda: self.do_cmd(self.startup)))
        self.appium_commands.append(Command("Stop Appium", lambda: self.do_cmd(self.close_appium)))
        self.appium_commands.append(Command("Toggle Multi-Edit", lambda: self.do_cmd(self.toggle_multi_edit)))
        self.other_commands.append(Command("Enable USB", lambda: self.do_cmd(self.usb_enable)))
        self.other_commands.append(
            Command("Force AOSP Downgrade to 2.3.12", lambda: self.do_cmd(self.force_aosp_downgrade)))
        self.other_commands.append(
            Command("Get Alpha Current Versions", lambda: self.do_cmd(self.get_alpha_current_versions)))
        self.other_commands.append(
            Command("Get Beta Current Versions", lambda: self.do_cmd(self.get_beta_current_versions)))
        self.other_commands.append(Command("Get Installed Versions", lambda: self.do_cmd(self.get_installed_versions)))
        self.other_commands.append(
            Command("Get Production Current Versions", lambda: self.do_cmd(self.get_prod_current_versions)))
        self.other_commands.append(Command("Install APK 1.0.10", lambda: self.do_cmd(lambda: self.install_apk('1.0.10'))))
        self.other_commands.append(Command("Install APK 1.3.6", lambda: self.do_cmd(lambda: self.install_apk('1.3.6'))))
        self.other_commands.append(Command("Reboot", lambda: self.do_cmd(self.reboot)))
        self.other_commands.append(Command("Remove APK Upgrades", lambda: self.do_cmd(remove_apk_upgrades)))
        self.other_commands.append(Command("Start Appium", lambda: self.do_cmd(self.open_appium)))

    def do_cmd(self, cmd):
        for btn in self.appium_btns:
            btn.configure(state=DISABLED)
        for btn in self.noappium_btns:
            btn.configure(state=DISABLED)
        self.update_idletasks()
        sleep(5)
        cmd()
        if self.appium_is_open:
            for btn in self.appium_btns:
                btn.configure(state=NORMAL)
            for i in range(self.appium_sub_menu_max_index):
                self.appium_sub_menu.entryconfig(i + 1, state=NORMAL)
            for btn in self.noappium_btns:
                btn.configure(state=DISABLED)
            for i in range(self.other_sub_menu_max_index):
                self.other_sub_menu.entryconfig(i + 1, state=DISABLED)
        else:
            for btn in self.appium_btns:
                btn.configure(state=DISABLED)
            for i in range(self.appium_sub_menu_max_index):
                self.appium_sub_menu.entryconfig(i + 1, state=DISABLED)
            for btn in self.noappium_btns:
                btn.configure(state=NORMAL)
            for i in range(self.other_sub_menu_max_index):
                self.other_sub_menu.entryconfig(i + 1, state=NORMAL)


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
        color = base_view.get_element_color_and_count('appium_gui', elem, color_list_index=0)
        print "first color and count: %s" % color
        color = base_view.get_element_color_and_count('appium_gui', elem, color_list_index=1)
        print "second color and count: %s" % color
        for color_name in ['favorite_on_color', 'favorite_off_color']:
            if base_view.color_match(color, cfg.colors['ContactsView'][color_name]):
                print color_name

    def click_element(self):
        text_index = self.elem_index.get()
        if text_index == '':
            return
        index = int(text_index)
        self.elems[index].click()

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

    def close_appium(self):
        print "Closing Appium...",
        base_view.close_appium()
        self.appium_is_open = False
        print "Done"

    @staticmethod
    def get_current_activity():
        print "current activity: " + base_view.driver.current_activity

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

    @staticmethod
    def login():
        print "Logging in...",
        login_view.login()
        print "Done"

    def restart_appium(self):
        print "Restarting Appium...",
        self.close_appium()
        self.open_appium()
        print "Done"

    @staticmethod
    def usb_enable():
        print "Enabling USB via spud port...",
        usb_enable()
        print "Done"

    @staticmethod
    def accept_tnc():
        print "accepting terms and conditions...",
        tnc_view.accept_tnc()
        print "Done"

    @staticmethod
    def startup():
        print "running startup...",
        base_view.startup()
        print "Done"

    @staticmethod
    def set_alpha_ota_server():
        print "Setting alpha OTA server...",
        user_view.goto_tab('Dial')
        user_view.set_ota_server('alpha')
        print "Done"

    def install_apk_1_0_10(self):
        print "Installing APK 1.0.10 using adb...",
        self.install_apk('1.0.10')
        print "Done"

    def install_apk_1_3_6(self):
        print "Installing APK 1.3.6 using adb...",
        self.install_apk('1.3.6')
        print "Done"

    @staticmethod
    def skip_walkthrough():
        print "skipping walkthrough"
        app_intro_view.skip_intro()

    def reboot(self):
        print "rebooting...",
        self.reboot()
        print "Done"

    @staticmethod
    def get_installed_versions(self):
        print "getting installed versions"
        aosp, app = get_installed_versions()
        print "aosp: %s, app: %s" % (aosp, app)

    @staticmethod
    def get_alpha_current_versions():
        print "getting current alpha versions"
        aosp, app = get_current_versions('alpha')
        print "aosp: %s, app: %s" % (aosp, app)

    @staticmethod
    def get_beta_current_versions():
        print "getting current beta versions"
        aosp, app = get_current_versions('beta')
        print "aosp: %s, app: %s" % (aosp, app)

    @staticmethod
    def get_prod_current_versions():
        print "getting current prod versions"
        aosp, app = get_current_versions('prod')
        print "aosp: %s, app: %s" % (aosp, app)

    @staticmethod
    def get_all_coworker_contacts():
        print "getting coworker contacts"
        contacts_group = cfg.site['Users']['R2d2User']['CoworkerContacts']
        nums = contacts_view.get_all_group_contacts(contacts_group)
        print repr(nums)

    @staticmethod
    def dial_advanced_settings():
        print "dialing advanced settings code...",
        dial_view.dial_advanced_settings()
        dial_view.touch_call_button()
        print "Done"

    @staticmethod
    def dial_alpha_ota(self):
        print "dialing alpha OTA code...",
        dial_view.dial_set_alpha_ota_server()
        dial_view.touch_call_button()
        print "Done"

    @staticmethod
    def dial_beta_ota():
        print "dialing beta OTA code...",
        dial_view.dial_set_beta_ota_server()
        dial_view.touch_call_button()
        print "Done"

    @staticmethod
    def dial_prod_ota():
        print "dialing prod OTA code...",
        dial_view.dial_set_production_ota_server()
        dial_view.touch_call_button()
        print "Done"

    @staticmethod
    def dial_show_ota():
        print "dialing show OTA code...",
        dial_view.dial_show_ota_server()
        dial_view.touch_call_button()
        print "Done"

    @staticmethod
    def toggle_multi_edit():
        print "Toggling Multi-Edit...",
        contacts_view.toggle_multi_edit()
        print "Done"

    @staticmethod
    def force_aosp_downgrade():
        print "Forcing AOSP Downgrade...",
        force_aosp_downgrade('2.3.12')
        print "Done"

    @staticmethod
    def get_xml(self):
        print "Getting XML and CSV...",
        xml = base_view.get_source()
        xml_dir = os.path.join(cfg.xml_folder, 'xml_appium_gui')
        try:
            os.makedirs(xml_dir)
        except OSError as e:
            # ignore 'File exists' error but re-raise any others
            if e.errno != 17:
                raise e
        xml_fullpath = os.path.join(xml_dir, 'appium_gui.xml')
        log.info("saving xml %s" % xml_fullpath)
        with open(xml_fullpath, 'w') as _f:
            _f.write(xml.encode('utf8'))
        xml_folder_to_csv()

        print "Done"

    @staticmethod
    def get_screenshot():
        print "Getting Screenshot...",
        base_view.get_screenshot_as_png('appium_gui', cfg.test_screenshot_folder)
        print "Done"

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

