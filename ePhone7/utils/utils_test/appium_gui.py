from ePhone7.utils.configure import cfg
from ePhone7.views import *
from time import sleep
from Tkinter import Tk, Frame, Button, Text, NORMAL, DISABLED, Scrollbar
import sys
cfg.set_site('vqda1', 'mm')


def reboot():
    print "rebooting..."
    user_view.click_named_element('PrefsButton')
    assert prefs_view.element_is_present('Preferences')
    prefs_view.hide_list_items()
    prefs_view.click_named_element('System')
    prefs_view.element_is_present('MenuItemNetworkText')
    prefs_view.click_named_element('MenuItemNetworkText')
    assert network_view.element_is_present('NetworkSettingsLabel')
    network_view.click_named_element('NetworkSaveAndReboot')
    assert network_view.element_is_present("VlanRebootAlert")
    base_view.close_appium()
    sleep(30)


def login():
    print "logging in"
    login_view.login()


def accept_tnc():
    print "accepting terms and conditions"
    tnc_view.accept_tnc()


def get_current_activity():
    print "current activity: " + base_view.driver.current_activity


def skip_walkthrough():
    print "skipping walkthrough"
    app_intro_view.skip_intro()


class Command(object):
    def __init__(self, text, fn):
        self.text = text
        self.fn = fn

commands = []
commands.append(Command("Get Current Activity", get_current_activity))
commands.append(Command("Log In", login))
commands.append(Command("Accept T&C", accept_tnc))
commands.append(Command("Skip Walkthrough", skip_walkthrough))


class ScrolledLogwin(Text):
    def __init__(self, parent, **kwargs):
        Text.__init__(self, parent, **kwargs)
        self.scrollback = 5000
        self.configure(state=DISABLED)
        self.sb = Scrollbar(self.master, command=self.yview)
        self["yscrollcommand"] = self.sb.set
        # self.hsb = Scrollbar(self.master, command=self.xview, orient=HORIZONTAL)
        # self["xscrollcommand"] = self.hsb.set
        self.sb.grid(row=0, column=1, sticky='ns', padx=5, pady=5)
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


class LogFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg='gray')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        print "parent = " + repr(parent)
        self.txt = ScrolledLogwin(self, width=80, height=10, name='cmd')
        self.txt.grid(row=0, column=0, sticky='news', padx=5, pady=5)

    def write(self, *args, **kwargs):
        self.txt.write(*args, **kwargs)

    def flush(self, *args, **kwargs):
        pass


class TestGui(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent, bg="tan")
        self.btns = []
        self.btn_frame = Frame(self, bg="cyan")
        row = None
        for row, cmd in enumerate(commands):
            btn = Button(self.btn_frame, text=cmd.text, command=cmd.fn, state=DISABLED)
            self.btns.append(btn)
            # print "button %s at row %s" % (cmd.text, row)
            btn.grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.quit = Button(self.btn_frame, text="Quit", command=self.quit)
        row += 1
        # print "button Quit at row %s" % row
        self.quit.grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.btn_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        self.logframe = LogFrame(self)
        sys.stdout = self.logframe
        # print "logframe at row %s" % row
        self.logframe.grid(row=1, column=0, padx=5, pady=5)
        self.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        print "Opening Appium...",
        self.update_idletasks()
        self.after(500, self.open_appium)

    def open_appium(self):
        base_view.open_appium()
        print "Done"
        for btn in self.btns:
            btn.configure(state=NORMAL)

    def __del__(self):
        base_view.close_appium()


root = Tk()
root.wm_title("Appium test utility")
app = TestGui(root)
app.mainloop()

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

