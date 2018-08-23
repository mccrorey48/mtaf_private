import os
from time import sleep, time
from selenium.common.exceptions import InvalidSelectorException
import mtaf_logging
from angular_actions import AngularActions
import threading
import json
from filters import get_filter
import errno
from mtaf.trace import Trace
import shutil
from bs4 import BeautifulSoup
from Tkinter import *
import tkfilebrowser
import tk_simple_dialog
from ttk import Combobox
from Queue import Queue
from PIL import Image as PIL_Image, ImageTk


angular_actions = AngularActions()
mtaf_logging.disable_console()
log = mtaf_logging.get_logger('mtaf.inspector')
re_dumpsys = re.compile('(?ms).*mCurrentFocus=\S+\s+\S+\s+([^/]+)/([^}]+)')
btn_default_bg = '#d9d9d9'
btn_select_bg = '#b97979'


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as _e:
        if _e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


class AutoIncrementer(object):
    # useful for keeping track of row and column assignments when building a GUI;
    # permits adding a widget in the middle of a group without having to reassign
    # the rows or columns in widgets that follow the added widget
    #
    # To Use:
    # - create an instance of AutoIncrementer
    # - to start a named row or column counter, give it an appropriate class member name
    #   and it will be automatically created, returning a zero value
    # - each time the value of the counter is used, it will be incremented by 1
    # - to set the value of the counter, just assign to it
    # - to skip rows or columns, use the "+=" operator
    #
    # Example:
    #   ai = AutoIncrementer()
    #   btn = Button(...)
    #   btn.grid(row=0, column=ai.btn_col)
    #   btn2 = Button(...)
    #   btn2.grid(row=0, column=ai.btn_col)
    #   btn3 = Button(...)
    #   # skip a couple of columns
    #   ai.btn_col += 2
    #   btn3.grid(row=0, column=ai.btn_col)

    def __init__(self):
        self.__dict__['counts'] = {}
        self.last_count = 0

    def __setattr__(self, name, value):
        if name == 'last_count':
            self.__dict__['last_count'] = value
        self.__dict__['counts'][name] = value

    def __getattr__(self, name):
        if name == 'last_count':
            return self.__dict__['last_count']
        if name not in self.__dict__['counts']:
            self.__dict__['counts'][name] = 0
        self.last_count = self.__dict__['counts'][name]
        self.__dict__['counts'][name] += 1
        return self.last_count


class MyDialog(tk_simple_dialog.Dialog):

    list = None
    devices = None

    def body(self, master):

        Label(master, text="Select Device:").grid(row=0)

        self.devices = master.master.master.devices
        self.list = Listbox(master, height=len(self.devices))
        for key in self.devices:
            self.list.insert(END, "%s: %s" % (key, self.devices[key]))
        self.list.grid(row=1)
        return self.list  # initial focus

    def apply(self):
        key = self.list.curselection()[0]
        self.devices = {0: self.devices[key]}


class ScrolledFrame(Frame):
    def __init__(self, parent, hsb=True, vsb=True, frame_label=''):
        Frame.__init__(self, parent, bg='green')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.canvas = Canvas(self, borderwidth=0, background="#ffffff")
        if len(frame_label):
            self.frame = LabelFrame(self.canvas, background="#ffffff", text=frame_label)
        else:
            self.frame = Frame(self.canvas, background="#ffffff")
        if hsb:
            self.hsb = Scrollbar(self, orient="horizontal", command=self.canvas.xview)
            self.canvas.configure(xscrollcommand=self.hsb.set)
        if vsb:
            self.vsb = Scrollbar(self, orient="vertical", command=self.canvas.yview)
            self.canvas.configure(yscrollcommand=self.vsb.set)

        if hsb:
            self.hsb.grid(row=1, column=0, sticky='ew')
        if vsb:
            self.vsb.grid(row=0, column=1, sticky='ns')
        self.canvas.grid(row=0, column=0, sticky='nsew')
        self.canvas.create_window((4,4), window=self.frame, anchor="nw",
                                  tags="self.frame")
        self.frame.bind("<Configure>", self.onFrameConfigure)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))



class ScrolledLogwin(Frame):
    def __init__(self, parent, height=20, label='', clear_button=False):
        Frame.__init__(self, parent)
        self.log_q = Queue()
        self.parent = parent
        self.title_bar = Frame(self)
        self.title_bar.label = Label(self.title_bar, text=label)
        self.title_bar.label.grid(row=0, column=0, sticky='ew')
        if clear_button:
            self.title_bar.clear_btn = Button(self.title_bar, text="clear window", command=self.clear,
                                              bg=btn_default_bg)
            self.title_bar.clear_btn.grid(row=0, column=1, padx=0, pady=0)
        self.title_bar.columnconfigure(0, weight=1)
        self.title_bar.grid(row=0, column=0, columnspan=2, sticky='ew')
        self.txt = Text(self, height=height)
        self.scrollback = 5000
        self.txt.configure(state=DISABLED)
        self.sb = Scrollbar(self, command=self.txt.yview)
        self.txt["yscrollcommand"] = self.sb.set
        self.txt.grid(row=1, column=0, sticky='nsew', padx=0, pady=0)
        self.sb.grid(row=1, column=1, sticky='ns', padx=0, pady=0)
        self.rowconfigure(1, weight=1)
        self.print_buf = ''
        self.read_q()

    def clear(self):
        self.txt.configure(state=NORMAL)
        self.txt.delete('1.0', END)
        self.txt.configure(state=DISABLED)

    def write(self, _txt):
        self.log_q.put(_txt)

    def read_q(self):
        while not self.log_q.empty():
            _txt = self.log_q.get()
            # old_stdout.write(">>%s<<" % _txt)
            log.debug("write: _txt = [%s], len=%d" % (repr(_txt), len(_txt)))
            if len(_txt) > 0 and _txt[-1] == '\n':
                eol = True
            else:
                eol = False
            lines = _txt.strip().split('\n')
            self.txt.configure(state=NORMAL)
            for line in lines[:-1]:
                self.txt.insert('end', line + '\n')
            if len(lines):
                self.txt.insert('end', lines[-1])
            if eol:
                self.txt.insert('end', '\n')
            # self.delete('0.0', 'end - %d lines' % self.scrollback)
            self.txt.see('end')
            # self.update_idletasks()
            self.txt.configure(state=DISABLED)
        self.after(100, self.read_q)


class MenuItem(object):
    def __init__(self, label, action, uses_browser):
        self.label = label
        self.action = action
        self.uses_browser = uses_browser


class MyMenu(Menu):
    def __init__(self, parent):
        Menu.__init__(self, parent)
        self.items = {}

    def add_submenu(self, label, menu_items):
        if label in self.items:
            submenu = self.items[label]["menu"]
        else:
            submenu = MyMenu(self)
            self.add_cascade(label=label, menu=submenu)
            self.items[label] = {"menu": submenu, "uses_browser": []}
        for i, item in enumerate(menu_items):
            submenu.add_command(label=item.label, command=item.action)
            self.items[label]["uses_browser"].append(item.uses_browser)

    def enable_items(self, browser_open):
        for label in self.items:
            for i in range(len(self.items[label]["uses_browser"])):
                uses_browser = self.items[label]["uses_browser"][i]
                if browser_open and (uses_browser is True or uses_browser is None):
                    self.items[label]["menu"].entryconfig(i + 1, state=NORMAL)
                elif (not browser_open) and (uses_browser is False or uses_browser is None):
                    self.items[label]["menu"].entryconfig(i + 1, state=NORMAL)
                else:
                    self.items[label]["menu"].entryconfig(i + 1, state=DISABLED)


class AttrFrame(Frame):
    index = None


class BottomFrame(Frame):
    mk_canvas = None


class ButtonFrame(Frame):
    find_frame = None


old_stdout = sys.stdout


class Inspector(Frame):
    menu_cmd_labels = {}

    def __init__(self, parent, gui_cfg):
        Frame.__init__(self, parent, bg="brown")
        self.parent = parent
        self.cfg = gui_cfg
        self.browser_btns = []
        self.browser_is_open = False
        self.add_cmd_btn = None
        self.automation_name = None
        self.clickable_element = None
        self.clicked_elems = {}
        self.cwin = None
        self.cwin_x = None
        self.cwin_y = None
        self.devices = []
        self.elem_index = None
        self.elem_indices = []
        self.elems = []
        self.elems_btns = []
        self.exec_cb = None
        self.exec_text = StringVar(name='exec_text')
        self.exec_history = {}
        self.find_button = None
        self.find_by_var = None
        self.find_value_var = StringVar(name='find')
        self.frame_element = None
        self.id_frame_btns = {}
        self.id_frame = None
        self.id_label = None
        self.ids = None
        self.ids = None
        self.im_canvas = None
        self.im_height = None
        self.im_width = None
        self.keycode_name = None
        self.last_cmd = ''
        self.locator_by_values = ['id', 'xpath', 'link text', "partial link text", "name", "tag name", "class name",
                                  "css selector"]
        self.locators = {}
        self.locator_css_type = StringVar()
        self.locator_part_cbs = []
        self.locator_full_cb = {}
        self.locator_text_cb = {}
        self.locator_text_val = StringVar()
        self.log_frame = None
        self.menu = None
        self.parent_element = None
        self.polygons = []
        self.processor_elems = {}
        self.script_btn_enable_states = {}
        self.script_fd = None
        self.script_file = StringVar()
        self.script_file.set(os.path.join(self.cfg['tmp_dir'], 'web_inspector_scripts', 'web_inspector_script.txt'))
        self.script_recording = False
        self.script_rec_btns = []
        self.script_running = False
        self.script_run_btns = []
        self.script_state = 'stopped'
        self.soup = None
        self.cmd_file = os.path.join(self.cfg['tmp_dir'], 'web_inspector_commands.json')
        self.loc_file = os.path.join(self.cfg['tmp_dir'], 'web_inspector_locators.json')
        self.rec_frame = None
        self.locator_req_text = IntVar()
        self.screenshot_file_name = 'web_inspector.png'
        self.script_btns = []
        self.swipe_ms_var = StringVar()
        self.swipe_y1_var = StringVar()
        self.swipe_y2_var = StringVar()
        self.tap_x_var = StringVar()
        self.tap_y_var = StringVar()
        self.text_to_send = None
        self.top_frames = []
        self.top_frame_row = 0
        self.use_parent = IntVar(name='use_parent')
        self.within_frame = IntVar()
        self.worker_thread = None
        parent.bind_all("<Button-4>", self.mouse_btn)
        parent.bind_all("<Button-5>", self.mouse_btn)

        try:
            with open(self.loc_file, 'r') as f:
                self.locators = json.loads(f.read())
        except (IOError, ValueError):
            pass

        try:
            with open(self.cmd_file, 'r') as f:
                self.exec_history = json.loads(f.read())
        except (IOError, ValueError):
            pass

        if 'values' not in self.exec_history:
            self.exec_history['values'] = []

        self.btn_frame = self.create_btn_frame()
        self.top_frames.append(self.btn_frame)
        self.top_frames.append(self.create_exec_frame())
        self.top_frames.append(self.create_log_frame())
        self.bottom_frame = self.create_bottom_frame()
        self.top_frames.append(self.bottom_frame)
        self.populate_top_frames()

        sys.stdout = self.log_frame

        self.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, padx=2, pady=2, sticky='nsew')
        for btn in self.browser_btns:
            btn.configure(state=DISABLED)
        self.user_cmds = {
            'Get Current Page Title': lambda: self.do_cmd(self.get_title),
            'Get Current URL': lambda: self.do_cmd(self.get_current_url),
            'Open Browser': lambda: self.do_cmd(self.open_browser),
            'Go To eConsole URL': lambda: self.do_cmd(self.goto_econsole),
            'Close Browser': lambda: self.do_cmd(self.close_browser)
        }
        self.create_menus(parent)

    def process_attrs(self, tag, tag_index, attrs, text):
        # use tag, attrs and text from beautiful soup representation of an element on the current page
        # to generate "css selector" values, then figure out what css selector qualifiers are required to
        # identify the right element
        by = 'css selector'
        css_selectors = []
        partial_values = []
        # convert attrs dict to an array of css selector qualifiers
        for key in attrs:
            if key == "href" and attrs[key] == "":
                return
            if type(attrs[key]) == list:
                try:
                    css_selectors.append('[%s="%s"]' % (key, ' '.join(attrs[key])))
                except TypeError:
                    pass
            else:
                css_selectors.append('[%s="%s"]' % (key, attrs[key]))
        # try each qualifier to see how many elements are returned
        for selector in css_selectors[:]:
            value = tag + selector
            try:
                elems = angular_actions.driver.find_elements(by, value)
                elems = filter(lambda x: x.is_displayed(), elems)
            except InvalidSelectorException:
                log.debug("removing invalid css selector %s" % selector)
                css_selectors.remove(selector)
            else:
                log.debug("len(elems) = %d: css_selector = %s" % (len(elems), selector))
                partial_values.append({'selector': selector, 'matches': len(elems)})
        # use all qualifiers together and save result in all_elems
        value = tag + ''.join(css_selectors)
        all_elems = []
        try:
            all_elems = angular_actions.driver.find_elements(by, value)
            all_elems = filter(lambda x: x.is_displayed(), all_elems)
        except InvalidSelectorException as e:
            print "got exception %s: by = %s, value = %s" % (e, by, value)
        # all qualifiers together should return at least one element
        # if len(all_elems) == 0:
        #     raise RuntimeError('no elements returned with css selector %s' % value)
        # filter out elements with zero size
        # elems = []
        # for elem in all_elems:
        #     if int(elem.size['width']) * int(elem.size['height']) > 0:
        #         elems.append(elem)
        required_text = None
        # if there are still multiple elements, narrow down the list to those that have the specified text value
        if len(all_elems) > 1:
            # print "multiple elements found, trying filter by text"
            for elem in all_elems[:]:
                if text and elem.text != text:
                    # print "removing element with text != %s" % text
                    all_elems.remove(elem)
            # if the text match reduces the count to one, save as "required_text"
            # if there are still multiple elements, print a notification and figure out how to deal with that later
            if len(all_elems) > 1:
                print 'expected one element, got %d using css value "%s"' % (len(all_elems), value)
            elif len(all_elems) == 1:
                required_text = text
            # raise RuntimeError('expected one element, got %d using css value "%s"' % (len(elems), value))
        # save characteristics of remaining elements in self.elems
        if tag not in self.processor_elems:
            self.processor_elems[tag] = []
        for elem in all_elems:
            location = all_elems[0].location
            size = elem.size
            area = int(size['width']) * int(size['height'])
            x1 = int(location['x'])
            y1 = int(location['y'])
            x2 = x1 + int(size['width'])
            y2 = y1 + int(size['height'])
            # only add elem to self.processor_elems[tag] if it isn't already there (with another index number)
            if x1 * self.cwin.scale < self.im_width and y1 * self.cwin.scale < self.im_height:
                new_processor_elem = {
                        'tag': tag,
                        'index': tag_index,
                        'by': by,
                        'value': value,
                        'geom': {'area': area, 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2},
                        'partial_values': partial_values,
                        'text': required_text
                    }
                elem_attrs = sorted([new_processor_elem[attr] for attr in new_processor_elem.keys() if attr != 'index'])
                for p_elem in self.processor_elems[tag]:
                    p_elem_attrs = sorted([p_elem[attr] for attr in p_elem.keys() if attr != 'index'])
                    if p_elem_attrs == elem_attrs:
                        break
                else:
                    self.processor_elems[tag].append(new_processor_elem)

    def get_url(self, url):
        angular_actions.get_url(url)

    def open_browser(self):
        self.save_last_cmd("self.open_browser()")
        angular_actions.open_browser()
        self.browser_is_open = True
        self.menu.enable_items(self.browser_is_open)
        self.elems = []
        print ">> open browser done"

    def goto_econsole(self):
        url = "http://staging-econsole.esihs.net"
        self.save_last_cmd("angular_actions.driver.get_url('%s')" % url)
        angular_actions.get_url(url)
        self.menu.enable_items(self.browser_is_open)
        self.elems = []
        print ">> go to eConsole done"

    def close_browser(self):
        self.save_last_cmd("self.close_browser()")
        angular_actions.close_browser()
        self.browser_is_open = False
        self.menu.enable_items(self.browser_is_open)
        # self.configure_find_button()
        self.elems = []
        print ">> close browser done"

    def get_title(self):
        self.save_last_cmd("self.get_title()")
        print angular_actions.driver.title

    def get_current_url(self):
        self.save_last_cmd("self.current_url()")
        print angular_actions.driver.current_url

    def populate_top_frames(self):
        for top_frame in self.top_frames:
            if hasattr(top_frame, 'expand_y') and top_frame.expand_y is True:
                self.grid_rowconfigure(self.top_frame_row, weight=1)
            top_frame.grid_forget()
            top_frame.grid(row=self.top_frame_row, column=0, padx=4, pady=2, sticky='news')
            self.top_frame_row += 1

    def change_script(self):
        self.update_script_state('changing')
        filename = tkfilebrowser.askopenfilename(initialdir=os.path.join(self.cfg['tmp_dir'], 'web_inspector_scripts'),
                                                 initialfile=os.path.basename(self.script_file.get()),
                                                 title="Select current script",
                                                 filetypes=(
                                                     (".txt files", "*.txt"),
                                                     ("all files", "*.*"))
                                                 )
        if filename:
            self.script_file.set(filename)
        self.update_script_state('stopped')

    def print_script(self):
        self.update_script_state('printing')
        filename = self.script_file.get()
        print '>> Printing contents of %s:' % self.script_file.get()
        try:
            with open(filename, 'r') as f:
                for line in f:
                    print line,
        except BaseException as e:
            print 'got exception: %s' % e
        print '>> print script done'
        self.update_script_state('stopped')

    def run_script(self):
        self.update_script_state('running')
        self.disable_buttons()
        self.update_idletasks()
        self.script_running = True
        filename = self.script_file.get()
        print ">> Running script file %s" % filename
        try:
            with open(filename, 'r') as f:
                try:
                    for line in f:
                        line = line.strip()
                        if line[0] == '#' or line[0] == '"':
                            continue
                        if not self.script_running:
                            break
                        print "exec: %s" % line
                        exec line
                except Exception as _e:
                    print "exec raised exception: %s" % _e
                    if self.browser_is_open:
                        self.close_browser()
        except BaseException as e:
            print "open(%s, 'r') got exception: %s" % e
        self.script_running = False
        self.enable_buttons()
        print '>> script file "%s" done' % filename
        self.update_script_state('stopped')

    def record_script(self):
        self.update_script_state('recording')
        filename = tkfilebrowser.asksaveasfilename(initialdir=os.path.join(self.cfg['tmp_dir'],
                                                                           'web_inspector_scripts'),
                                                   initialfile=os.path.basename(self.script_file.get()),
                                                   title="Select exising file, or enter filename to save recording",
                                                   filetypes=(
                                                       (".txt files", "*.txt"),
                                                       ("all files", "*.*"))
                                                   )
        if filename:
            self.script_file.set(filename)
            print ">> Recording commands to %s" % self.script_file.get()
            self.script_fd = open(self.script_file.get(), 'w')
            if len(self.exec_text.get().strip()) > 0:
                self.add_cmd_btn.configure(state=NORMAL)
        else:
            self.update_script_state('stopped')

    def add_to_script(self):
        self.update_script_state('recording')
        filename = tkfilebrowser.askopenfilename(initialdir=os.path.join(self.cfg['tmp_dir'], 'web_inspector_scripts'),
                                                 initialfile=os.path.basename(self.script_file.get()),
                                                 title="Select script to add new commands",
                                                 filetypes=(
                                                     (".txt files", "*.txt"),
                                                     ("all files", "*.*"))
                                                 )
        if filename:
            self.script_file.set(filename)
            print ">> Adding commands to %s" % self.script_file.get()
            self.script_fd = open(self.script_file.get(), 'a')
            if len(self.exec_text.get().strip()) > 0:
                self.add_cmd_btn.configure(state=NORMAL)
        else:
            self.update_script_state('stopped')

    def copy_script(self):
        self.update_script_state('recording')
        fname = tkfilebrowser.asksaveasfilename(initialdir=os.path.join(self.cfg['tmp_dir'], 'web_inspector_scripts'),
                                                initialfile=os.path.basename(self.script_file.get()),
                                                title="Copy current script to file: ",
                                                filetypes=(
                                                    (".txt files", "*.txt"),
                                                    ("all files", "*.*"))
                                                )
        if fname:
            if fname == self.script_file.get():
                print "not copying %s to same filename"
            else:
                print "copying %s to %s... " % (self.script_file.get(), fname),
                shutil.copyfile(self.script_file.get(), fname)
                self.script_file.set(fname)
                print ">> script copy done"
        self.update_script_state('stopped')

    def stop_script(self):
        # if running, stop executing script lines
        self.script_running = False
        # if recording or adding, stop
        if self.script_fd is not None:
            self.script_fd.close()
            self.script_fd = None
        self.add_cmd_btn.configure(state=DISABLED)
        self.update_script_state('stopped')
        print ">> Stopped recording to %s" % self.script_file.get()

    def add_cmd_to_script(self):
        cmd = self.exec_text.get().strip()
        if len(cmd):
            if self.script_fd is None:
                print 'script not open for recording, select "Record New" or "Add to Script"'
            else:
                self.script_fd.write(cmd + '\n')
                print 'added "%s" to current script' % cmd

    def check_thread(self):
        if self.worker_thread is None:
            return
        # there is a worker thread;
        # if it has died, set to None and enable buttons
        # if it is still alive, call "after" to check again in 100 ms
        if self.worker_thread.is_alive():
            self.after(100, self.check_thread)
            return
        else:
            log.debug(">> worker thread done: %s" % self.worker_thread.name)
            self.worker_thread = None
            # if do_cmd thread is done, re-enable the menubar dropdowns
            self.enable_buttons()

    def enable_buttons(self):
        for i in range(len(self.menu.items)):
            self.menu.entryconfig(i + 1, state=NORMAL)
        if self.browser_is_open:
            for btn in self.browser_btns:
                btn.configure(state=NORMAL)
        if self.elems is not None and len(self.elems) > 0:
            for btn in self.elems_btns:
                btn.configure(state=NORMAL)
        # depending on self.browser_is_enabled value, enable/disable dropdown menu items
        self.menu.enable_items(self.browser_is_open)
        self.update_script_state()

    def update_script_state(self, state=None):
        if state is not None:
            self.script_state = state
        for btn in self.script_btn_enable_states:
            if self.script_state in self.script_btn_enable_states[btn]:
                btn.configure(state=NORMAL)
            else:
                btn.configure(state=DISABLED)

    def create_bottom_frame(self):
        ai = AutoIncrementer()
        bottom_frame = BottomFrame(self, bg="tan")
        bottom_frame.script_frame = Frame(bottom_frame, bg="brown")
        bottom_frame.script_frame.script_label = Label(bottom_frame.script_frame, text="Current Script:")
        bottom_frame.script_frame.script_label.grid(row=0, column=0, sticky='e', padx=0, pady=2)
        bottom_frame.script_frame.script_name = Entry(bottom_frame.script_frame, textvariable=self.script_file,
                                                      width=75, state='readonly')
        bottom_frame.script_frame.script_name.grid(row=0, column=1, padx=4, pady=2, columnspan=6, sticky='news')

        btn = Button(bottom_frame.script_frame, text="Record New", bg=btn_default_bg, command=self.record_script)
        btn.grid(row=1, column=ai.col, sticky='ew', padx=4, pady=2)
        self.script_btns.append(btn)
        bottom_frame.script_frame.record_script = btn
        self.script_btn_enable_states[btn] = "stopped"

        btn = Button(bottom_frame.script_frame, text="Stop Recording", bg=btn_default_bg, command=self.stop_script,
                     state=DISABLED)
        btn.grid(row=1, column=ai.col, sticky='ew', padx=4, pady=2)
        self.script_btns.append(btn)
        bottom_frame.script_frame.stop_script = btn
        self.script_btn_enable_states[btn] = "recording"

        btn = Button(bottom_frame.script_frame, text="Print", bg=btn_default_bg, command=self.print_script)
        btn.grid(row=1, column=ai.col, sticky='ew', padx=4, pady=2)
        self.script_btns.append(btn)
        bottom_frame.script_frame.print_script = btn
        self.script_btn_enable_states[btn] = "stopped"

        btn = Button(bottom_frame.script_frame, text="Run", bg=btn_default_bg, command=self.run_script)
        btn.grid(row=1, column=ai.col, sticky='ew', padx=4, pady=2)
        self.script_btns.append(btn)
        bottom_frame.script_frame.run_script = btn
        self.script_btn_enable_states[btn] = "stopped"

        btn = Button(bottom_frame.script_frame, text="Add to Script", bg=btn_default_bg, command=self.add_to_script)
        btn.grid(row=1, column=ai.col, sticky='ew', padx=4, pady=2)
        self.script_btns.append(btn)
        bottom_frame.script_frame.add_to_script = btn
        self.script_btn_enable_states[btn] = "stopped"

        btn = Button(bottom_frame.script_frame, text="Copy", bg=btn_default_bg, command=self.copy_script)
        btn.grid(row=1, column=ai.col, sticky='ew', padx=4, pady=2)
        self.script_btns.append(btn)
        bottom_frame.script_frame.copy_script = btn
        self.script_btn_enable_states[btn] = "stopped"

        btn = Button(bottom_frame.script_frame, text="Change Current", bg=btn_default_bg, command=self.change_script)
        btn.grid(row=1, column=ai.col, sticky='ew', padx=4, pady=2)
        self.script_btns.append(btn)
        bottom_frame.script_frame.change_script = btn
        self.script_btn_enable_states[btn] = "stopped"

        bottom_frame.script_frame.grid(row=0, column=0, sticky='w')
        bottom_frame.grid_columnconfigure(0, weight=1)
        bottom_frame.Quit = Button(bottom_frame, text="Quit", bg=btn_default_bg,
                                   command=self.close_and_quit)
        bottom_frame.Quit.grid(row=0, column=1, sticky='se', padx=2, pady=2)
        return bottom_frame

    @Trace(log)
    def create_log_frame(self):
        pw = PanedWindow(self, orient=VERTICAL, bg='brown')
        self.log_frame = ScrolledLogwin(pw, height=self.cfg['log_window_height'], label='standard output',
                                        clear_button=True)
        self.log_frame.grid_columnconfigure(0, weight=1)
        pw.add(self.log_frame, stretch='always')
        rec_frame = ScrolledLogwin(pw, height=self.cfg['rec_window_height'], label='recorded text')
        self.rec_frame = rec_frame
        rec_frame.grid_columnconfigure(0, weight=1)
        pw.add(rec_frame, stretch='always')
        pw.expand_y = True
        return pw

    @staticmethod
    def defocus(event):
        event.widget.selection_clear()

    def create_exec_frame(self):
        ai = AutoIncrementer()
        exec_frame = Frame(self, bg="brown")
        exec_frame.exec_btn = Button(exec_frame, text="exec:", command=lambda: self.do_cmd(self.exec_code),
                                     bg=btn_default_bg, state=NORMAL)
        exec_frame.exec_btn.grid(row=0, column=ai.exec_col)
        self.exec_cb = Combobox(exec_frame, width=60, values=self.exec_history['values'], textvariable=self.exec_text)
        cb_col = ai.exec_col
        self.exec_cb.grid(row=0, column=cb_col, sticky='news')
        self.exec_text.trace('w', self.trace_callback)
        exec_frame.capture = Button(exec_frame, text="capture view", command=lambda: self.do_cmd(self.capture_view),
                                 bg=btn_default_bg, state=NORMAL)
        self.browser_btns.append(exec_frame.capture)
        exec_frame.capture.grid(row=0, column=ai.exec_col)
        exec_frame.last_cmd = Button(exec_frame, text="get last cmd", command=self.get_last_cmd,
                                     bg=btn_default_bg, state=NORMAL)
        exec_frame.last_cmd.grid(row=0, column=ai.exec_col)
        self.add_cmd_btn = Button(exec_frame, text="add to script", command=self.add_cmd_to_script,
                                  bg=btn_default_bg, state=DISABLED)
        self.add_cmd_btn.grid(row=0, column=ai.exec_col)
        exec_frame.columnconfigure(cb_col, weight=1)
        return exec_frame

    def exec_code(self):
        text = self.exec_text.get().strip()
        if len(text):
            self.save_last_cmd(text)
            if text not in self.exec_history['values']:
                self.exec_history['values'].insert(0, text)
                self.exec_history['values'] = self.exec_history['values'][:20]
                self.exec_cb.configure(values=self.exec_history['values'])
            try:
                exec text
            except Exception as _e:
                print "exec raised exception: %s" % _e
                if self.browser_is_open:
                    self.close_browser()

    def trace_callback(self, *_args):
        if _args[0] == 'exec_text':
            exec_text = self.exec_text.get().strip()
            # print "exec_text: %s" % exec_text
            if len(exec_text) > 0 and self.script_fd is not None:
                self.add_cmd_btn.configure(state=NORMAL)
            else:
                self.add_cmd_btn.configure(state=DISABLED)
        elif _args[0] == 'find':
            find_value = self.find_value_var.get().strip()
            # print "find_value: %s" % find_value
            if len(find_value):
                self.find_button.configure(bg=btn_select_bg, activebackground=btn_select_bg, state=NORMAL)
            else:
                self.find_button.configure(bg=btn_default_bg, activebackground=btn_default_bg, state=DISABLED)

    def create_btn_frame(self):
        ai = AutoIncrementer()
        btn_frame = ButtonFrame(self, bg="brown")

        btn_frame.find_frame = Frame(btn_frame, bg='tan')
        btn_frame.find_frame.grid(row=ai.bf_row, column=0, sticky='ew', padx=2, pady=2)
        btn = Button(btn_frame.find_frame, text="find elements:", bg=btn_default_bg,
                     command=lambda: self.do_cmd(self.find_elements_with_settings), state=DISABLED)
        self.find_button = btn
        self.browser_btns.append(btn)
        btn.grid(row=0, column=ai.ffr, padx=2, pady=2, sticky='n')

        self.find_by_var = StringVar()
        self.find_by_var.set(self.locator_by_values[0])
        btn_frame.find_frame.by = Combobox(btn_frame.find_frame, width=16, state='readonly', takefocus=False,
                                           values=self.locator_by_values, textvariable=self.find_by_var)
        self.browser_btns.append(btn_frame.find_frame.by)
        btn_frame.find_frame.by.bind('<<ComboboxSelected>>', self.update_find_widgets)
        btn_frame.find_frame.by.bind("<FocusIn>", self.defocus)
        btn_frame.find_frame.by.grid(row=0, column=ai.ffr, padx=2, pady=2, sticky='n')

        btn_frame.find_frame.cbs = Frame(btn_frame.find_frame, bg='tan')
        btn_frame.find_frame.cbs.grid(row=0, column=ai.ffr, padx=2, pady=2, sticky='n')

        btn_frame.find_frame.loc = Frame(btn_frame.find_frame)
        btn_frame.find_frame.loc.grid_columnconfigure(1, weight=1)
        loc_column = ai.ffr
        btn_frame.find_frame.loc.grid(row=0, column=loc_column, padx=2, pady=2, sticky='new')
        btn_frame.find_frame.grid_columnconfigure(loc_column, weight=1)

        self.use_parent.set(0)
        self.use_parent.trace('w', self.trace_callback)
        btn_frame.find_frame.cbs.use_parent = Checkbutton(btn_frame.find_frame.cbs, text='from Parent',
                                                          variable=self.use_parent, state=DISABLED)
        btn_frame.find_frame.cbs.use_parent.grid(row=0, column=0, padx=2, pady=2, sticky='ew')

        self.within_frame.set(0)
        btn_frame.find_frame.cbs.within_frame = Checkbutton(btn_frame.find_frame.cbs, text='within frame',
                                                            variable=self.within_frame, state=DISABLED)
        btn_frame.find_frame.cbs.within_frame.grid(row=1, column=0, padx=2, pady=2, sticky='ew')

        self.find_value_var.trace('w', self.trace_callback)
        btn_frame.find_frame.loc.value = Combobox(btn_frame.find_frame.loc, width=60,
                                                  values=self.get_filtered_locator_keys(),
                                                  textvariable=self.find_value_var)
        self.browser_btns.append(btn_frame.find_frame.loc.value)
        btn_frame.find_frame.loc.value.bind('<<ComboboxSelected>>', self.update_find_frame)
        btn_frame.find_frame.loc.value.bind("<FocusIn>", self.defocus)
        btn_frame.find_frame.loc.hsb = Scrollbar(btn_frame.find_frame.loc, orient=HORIZONTAL,
                                                 command=btn_frame.find_frame.loc.value.xview)
        btn_frame.find_frame.loc.value["xscrollcommand"] = btn_frame.find_frame.loc.hsb.set
        btn_frame.find_frame.loc.value.grid(row=0, column=0, padx=2, pady=0, sticky='ew', columnspan=2)
        btn_frame.find_frame.loc.hsb.grid(row=1, column=0, sticky='ew', columnspan=2)

        self.locator_req_text.set(0)
        btn_frame.find_frame.loc.req_text = Checkbutton(btn_frame.find_frame.loc, variable=self.locator_req_text,
                                                        text='Require text:', state=DISABLED)
        btn_frame.find_frame.loc.req_text.grid(row=2, column=0, padx=2, pady=2, sticky='w')
        self.browser_btns.append(btn_frame.find_frame.loc.req_text)
        btn_frame.find_frame.loc.text_val = Entry(btn_frame.find_frame.loc, textvariable=self.locator_text_val)
        btn_frame.find_frame.loc.text_val.grid(row=2, column=1, padx=2, pady=2, sticky='ew')
        self.browser_btns.append(btn_frame.find_frame.loc.text_val)

        btn_frame.attr_frame = AttrFrame(btn_frame, bg='tan')
        btn_frame.attr_frame.grid(row=ai.bf_row, column=0, sticky='ew', padx=2, pady=2)
        btn_frame.attr_frame.index_label = Label(btn_frame.attr_frame, text="select elem:", bg="tan")
        self.elems_btns.append(btn_frame.attr_frame.index_label)
        btn_frame.attr_frame.index_label.grid(row=0, column=ai.atf_r1, padx=2, pady=2, sticky='e')
        self.elem_index = StringVar()
        self.elem_index.set('')
        btn_frame.attr_frame.index = Combobox(btn_frame.attr_frame, width=6, values=[], textvariable=self.elem_index)
        self.elems_btns.append(btn_frame.attr_frame.index)
        btn_frame.attr_frame.index.grid(row=0, column=ai.atf_r1, padx=2, pady=2, sticky='e')
        btn = Button(btn_frame.attr_frame, text="get elem attributes", bg=btn_default_bg, command=self.get_elem_attrs,
                     state=DISABLED, padx=1)
        self.elems_btns.append(btn)
        btn.grid(row=0, column=ai.atf_r1, padx=2, pady=2)
        btn = Button(btn_frame.attr_frame, text="click elem", bg=btn_default_bg, command=self.click_element,
                     state=DISABLED, padx=1)
        self.elems_btns.append(btn)
        btn.grid(row=0, column=ai.atf_r1, padx=2, pady=2)
        btn = Button(btn_frame.attr_frame, text="set parent", bg=btn_default_bg, command=self.set_parent,
                     state=DISABLED, padx=1)
        self.elems_btns.append(btn)
        btn.grid(row=0, column=ai.atf_r1, padx=2, pady=2)
        btn = Button(btn_frame.attr_frame, text="set frame", bg=btn_default_bg, command=self.set_frame,
                     state=DISABLED, padx=1)
        self.elems_btns.append(btn)
        btn.grid(row=0, column=ai.atf_r1, padx=2, pady=2)
        btn = Button(btn_frame.attr_frame, text="clear elem", bg=btn_default_bg, command=self.clear_element,
                     state=DISABLED, padx=1)
        self.elems_btns.append(btn)
        btn.grid(row=1, column=ai.atf_r2, padx=2, pady=2)
        btn = Button(btn_frame.attr_frame, text="input text", bg=btn_default_bg, command=self.input_text,
                     state=DISABLED, padx=1)
        self.elems_btns.append(btn)
        btn.grid(row=1, column=ai.atf_r2, padx=2, pady=2)
        frame = Frame(btn_frame.attr_frame, bg='tan')
        frame.columnconfigure(0, weight=1)
        self.text_to_send = StringVar()
        entry = Entry(frame, textvariable=self.text_to_send, state=DISABLED)
        self.elems_btns.append(entry)
        entry.grid(row=0, column=0, sticky='ew')
        btn = Button(frame, text='X', command=self.clear_text_to_send, padx=0, pady=0)
        btn.grid(row=0, column=1)
        self.elems_btns.append(btn)
        frame.grid(row=1, column=ai.atf_r2, padx=2, pady=2, columnspan=3, sticky='ew')
        btn = Button(btn_frame.attr_frame, text="input ENTER", bg=btn_default_bg, command=self.input_enter,
                     state=DISABLED, padx=1)
        self.elems_btns.append(btn)
        ai.atf_r2 += 2
        btn.grid(row=1, column=ai.atf_r2, columnspan=2, padx=2, pady=2, sticky='w')

        btn_frame.grid_columnconfigure(0, weight=1)
        return btn_frame

    def clear_text_to_send(self):
        self.text_to_send.set('')

    def update_find_frame(self, event):
        value = self.find_value_var.get().split(':', 1)[1]
        self.find_value_var.set(value)
        if value in self.locators:
            self.find_by_var.set(self.locators[value]["by"])
            self.update_find_widgets(None)
            if self.parent_element is not None:
                self.use_parent.set(self.locators[self.find_value_var.get()]["use_parent"])
            else:
                self.use_parent.set(0)

    def make_menu_items(self, menu_items):
        return [MenuItem(item['label'], self.user_cmds[item['label']], item['uses_browser']) for item in menu_items]

    def create_menus(self, parent):
        menu_items = {
            'Browser Actions': [
                {'label': 'Open Browser', 'uses_browser': False},
                {'label': 'Go To eConsole URL', 'uses_browser': True},
                {'label': 'Get Current Page Title', 'uses_browser': True},
                {'label': 'Get Current URL', 'uses_browser': True},
                {'label': 'Close Browser', 'uses_browser': True}
            ]
        }
        self.menu = MyMenu(parent)
        for menu_label in menu_items:
            self.menu.add_submenu(menu_label, self.make_menu_items(menu_items[menu_label]))
        # depending on self.browser_is_enabled value, enable/disable dropdown menu items
        self.menu.enable_items(self.browser_is_open)
        parent.config(menu=self.menu)

    def close_and_quit(self):
        if self.browser_is_open:
            self.close_browser()
            self.update_idletasks()
            self.browser_is_open = False
        with open(self.loc_file, 'w') as f:
            f.write(json.dumps(self.locators, sort_keys=True, indent=4, separators=(',', ': ')))
        with open(self.cmd_file, 'w') as f:
            f.write(json.dumps(self.exec_history, sort_keys=True, indent=4, separators=(',', ': ')))
        self.quit()

    def do_cmd(self, cmd):
        if self.worker_thread is not None:
            print "worker thread busy: %s" % cmd.__name__
        else:
            # disable the menubar dropdowns and action buttons while thread is running
            self.disable_buttons()
            self.update_idletasks()
            self.worker_thread = threading.Thread(target=cmd, name=cmd.__name__)
            self.worker_thread.start()
            log.debug("worker thread started: %s" % cmd.__name__)
            self.after(100, self.check_thread)

    def disable_buttons(self):
        for btn in self.browser_btns:
            btn.configure(state=DISABLED)
        for btn in self.elems_btns:
            btn.configure(state=DISABLED)
        for i in range(len(self.menu.items)):
            self.menu.entryconfig(i + 1, state=DISABLED)
        for btn in self.script_btns:
            btn.configure(state=DISABLED)

    def update_find_widgets(self, event):
        find_by = self.find_by_var.get()
        # if (find_by == 'id') and self.parent_element is not None:
        if self.parent_element is not None:
            self.btn_frame.find_frame.cbs.use_parent.configure(state=NORMAL)
        else:
            self.btn_frame.find_frame.cbs.use_parent.configure(state=DISABLED)
            self.use_parent.set(0)
        if find_by[-11:] == 'locator_all' and self.frame_element is not None:
            self.btn_frame.find_frame.cbs.within_frame.configure(state=NORMAL)
        else:
            self.btn_frame.find_frame.cbs.within_frame.configure(state=DISABLED)

    def find_elements_with_driver(self, locator):
        try:
            angular_actions.wait_until_page_ready()
            by = locator['by']
            value = locator['value']
            if self.use_parent.get():
                elems = self.parent_element.find_elements(by, value)
            else:
                elems = angular_actions.driver.find_elements(by, value)
            elems = filter(lambda x: x.is_displayed(), elems)
            return elems
        except InvalidSelectorException as e:
            print 'got exception %s' % e

    def get_filtered_locator_keys(self):
        sorted_keys = sorted(self.locators.keys(), key=lambda x: self.locators[x]['time'], reverse=True)
        filtered_keys = filter(lambda x: self.locators[x]['by'] in self.locator_by_values, sorted_keys)
        return ["%s:%s" % (self.locators[key]['by'], key) for key in filtered_keys]

    def update_locator_list(self, locator=None):
        self.btn_frame.find_frame.by.configure(values=self.locator_by_values)
        # - find_elements passes in a locator value, which is added to self.locators
        # - the find element "by" combobox will be updated and the "value" combobox locator list will be filtered,
        #   according  to the current value of self.locator_by_values
        if locator is not None:
            if locator['value'] in self.locators.keys():
                self.locators[locator['value']]['time'] = time()
            else:
                self.locators[locator['value']] = {"by": locator['by'], "use_parent": locator['use_parent'],
                                                   "time": time()}
        sorted_keys = sorted(self.locators.keys(), key=lambda x: self.locators[x]['time'], reverse=True)
        # only keep 50 locators
        for key in sorted_keys[50:]:
            del self.locators[key]
            sorted_keys.pop()
        self.btn_frame.find_frame.loc.value.configure(value=self.get_filtered_locator_keys())

    def find_elements_with_settings(self):
        locator = {
            'by': self.find_by_var.get(),
            'value': self.find_value_var.get(),
            'use_parent': bool(self.use_parent.get())
        }
        if self.locator_req_text.get():
            locator['text'] = self.locator_text_val.get()
        self.update_locator_list(locator)
        # if locator['by'][-7:] == 'locator' or locator['by'][-11:] == 'locator_all':
        #     self.elems = self.find_elements_by_locator_name(locator)
        # else:
        self.find_elements_by_locator(locator)

    def find_elements_by_locator(self, locator):
        self.save_last_cmd("self.find_elements_by_locator(%s)" % locator)
        self.elems = self.find_elements_with_driver(locator)
        # keep frame element setting if using "by" value ending in '*_locator'
        self.frame_element = None
        self.within_frame.set(0)
        if self.locator_req_text.get():
            self.elems = filter(get_filter('text_all', text=self.locator_text_val.get()), self.elems)
        _msg = "%s element%s found" % (len(self.elems), '' if len(self.elems) == 1 else 's')
        print _msg
        elem_indices = [str(i) for i in range(len(self.elems))]
        self.btn_frame.attr_frame.index.configure(values=elem_indices)
        if len(elem_indices):
            self.elem_index.set('0')
        else:
            self.elem_index.set('')
        self.parent_element = None
        self.btn_frame.find_frame.cbs.use_parent.configure(state=DISABLED)
        self.use_parent.set(0)
        self.update_find_widgets(None)

    def get_elem_attrs(self):
        text_index = self.elem_index.get()
        if text_index == '':
            return
        index = int(text_index)
        elem = self.elems[index]
        script = 'var items = {};' \
            + 'for (index = 0; index < arguments[0].attributes.length; ++index) ' \
            + '{ items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value };' \
            + 'return items;'
        self.save_last_cmd('angular_actions.driver.execute_script(%s, self.elems(%s)' % (script, index))
        attrs = angular_actions.driver.execute_script(script, elem)
        print "\nattributes for element %d:" % index
        for key in attrs.keys():
            print "%s: %s" % (key, attrs[key])

    def click_element(self):
        text_index = self.elem_index.get()
        if text_index == '':
            return
        index = int(text_index)
        self.click_element_by_index(index)

    def get_last_cmd(self):
        self.exec_text.set(self.last_cmd)

    def save_last_cmd(self, cmd):
        if cmd != self.last_cmd:
            self.last_cmd = cmd
            print "last_cmd = %s" % cmd

    def click_element_by_index(self, index):
        self.save_last_cmd('self.click_element_by_index(%s)' % index)
        self.elems[index].click()

    def clear_element(self):
        text_index = self.elem_index.get()
        if text_index == '':
            return
        index = int(text_index)
        self.save_last_cmd('self.elems[%d].clear()' % index)
        self.elems[index].clear()

    def set_parent(self):
        text_index = self.elem_index.get()
        if text_index == '':
            return
        index = int(text_index)
        self.save_last_cmd('self.parent_element = self.elems[%d]' % index)
        self.parent_element = self.elems[index]
        self.update_find_widgets(None)

    def set_frame(self):
        text_index = self.elem_index.get()
        if text_index == '':
            return
        index = int(text_index)
        self.save_last_cmd('self.frame_element = self.elems[%d]' % index)
        self.frame_element = self.elems[index]
        self.update_find_widgets(None)

    def input_text(self):
        text_index = self.elem_index.get()
        if text_index == '':
            return
        index = int(text_index)
        text = self.text_to_send.get()
        self.save_last_cmd('self.input_text_to_element_index(%s, %d)' % (text, index))
        self.input_text_to_element_index(text, index)

    def input_text_to_element_index(self, text, index):
        try:
            elem = self.elems[index]
            elem.clear()
            terms = text.split('\\n')
            while len(terms):
                value = terms.pop(0)
                if len(value):
                    elem.send_keys(value)
                if len(terms):
                    elem.send_keys('\n')
        except BaseException as _e:
            print "got exception %s" % _e
        self.update_find_widgets(None)

    def input_enter(self):
        text_index = self.elem_index.get()
        if text_index == '':
            return
        index = int(text_index)
        self.save_last_cmd("self.elems[%d].send_keys('\n')" % index)
        try:
            self.elems[index].send_keys('\n')
        except BaseException as _e:
            print "got exception %s" % _e
        self.update_find_widgets(None)

    def capture_view(self):
        self.soup = BeautifulSoup(angular_actions.driver.page_source, 'html.parser')
        self.create_cwin()

        class TagInfo(object):
            def __init__(self, name, color, width):
                self.name = name
                self.color = color
                self.width = width

        tag_infos = [
            TagInfo('input', 'orange', 3),
            TagInfo('button', 'purple', 2),
            TagInfo('a', 'yellow', 1)
        ]
        self.processor_elems = {}
        for tag_info in tag_infos:
            old_num_proc_elems = 0
            elems = self.soup(tag_info.name)
            # print "number of %s elements: %d" % (tag_info.name, len(elems))
            for i, elem in enumerate (elems):
                self.process_attrs(tag_info.name, i, elem.attrs, elem.text.strip())
                num_proc_elems = len(self.processor_elems[tag_info.name])
                if num_proc_elems != old_num_proc_elems:
                    # print "added element %d: %s" % (i, elem)
                    old_num_proc_elems = num_proc_elems
        for tag_info in tag_infos:
            if tag_info.name in self.processor_elems:
                self.draw_outlines(self.processor_elems[tag_info.name], color=tag_info.color, clear=False,
                                   width=tag_info.width)

    def get_screenshot(self):
        print "Getting Screenshot ...",
        img_path = os.path.join(self.cfg["screenshot_dir"], self.screenshot_file_name)
        log.debug("saving screenshot to %s" % img_path)
        angular_actions.driver.get_screenshot_as_file(img_path)
        print ">> get screenshot done"

    @staticmethod
    def log_action(spud_serial, action):
        (reply, elapsed, groups) = spud_serial.do_action(action)
        lines = reply.split('\n')
        log.debug('cmd: %s\nelapsed: [%5.3f s]  \necho: "%s"\n' %
                  (action['cmd'], elapsed, repr(lines[0].encode('string_escape'))))
        for line in lines[1:]:
            log.debug(' '*7 + line.encode('string_escape'))

    @Trace(log)
    def create_cwin(self, reuse=False):
        if self.cwin is not None:
            self.cwin.destroy()
        self.cwin = Frame(self.parent, bg='brown')
        self.cwin.grid(row=0, column=1, sticky='ns')
        self.cwin.rowconfigure(1, weight=1)
        if not reuse:
            self.get_screenshot()
        image = PIL_Image.open(os.path.join(self.cfg['screenshot_dir'], self.screenshot_file_name))
        self.cwin.scale = 700.0 / max(image.height, image.width)
        self.im_width = int(image.width * self.cwin.scale)
        self.im_height = int(image.height * self.cwin.scale)
        small = image.resize((self.im_width, self.im_height))
        self.cwin.canvas_borderwidth = 8
        self.im_canvas = Canvas(self.cwin, height=self.im_height, width=self.im_width, bg='darkgrey',
                                borderwidth=self.cwin.canvas_borderwidth)
        self.im_canvas.photo = ImageTk.PhotoImage(small)
        self.im_canvas.create_image(self.im_width/2 + self.cwin.canvas_borderwidth,
                                    self.im_height/2 + self.cwin.canvas_borderwidth,
                                    image=self.im_canvas.photo)
        self.im_canvas.grid(row=0, column=0, sticky='n')
        self.im_canvas.bind('<Button-1>', self.mouse_btn)
        self.im_canvas.bind('<Button-2>', self.mouse_btn)
        self.im_canvas.bind('<Button-3>', self.mouse_btn)
        self.im_canvas.bind('<Button-4>', self.mouse_btn)
        self.im_canvas.bind('<Button-5>', self.mouse_btn)
        self.im_canvas.bind('<B1-Motion>', self.mouse_btn)
        self.im_canvas.bind('<ButtonRelease-1>', self.mouse_btn)
        # self.cwin.loc_frame = LabelFrame(self.cwin, width=600, height=300, text='Locator Options')
        self.cwin.loc_frame = ScrolledFrame(self.cwin, frame_label='Locator Options')
        # self.cwin.loc_frame.type_frame = Frame(self.cwin.loc_frame)
        # self.cwin.loc_frame.type_frame.grid(row=0, column=0, sticky='w')
        # self.cwin.loc_frame.attr_frame = Frame(self.cwin.loc_frame)
        # self.cwin.loc_frame.attr_frame.grid(row=1, column=0)
        # # self.cwin.loc_frame.grid(row=1, column=0, sticky='nsew')
        # self.cwin.scroll_frame.grid(row=0, column=0)
        # self.cwin.loc_frame.grid(row=0, column=0, sticky='nsew')
        self.cwin.loc_frame.grid(row=1, column=0, sticky='nsew')
        self.populate(self.cwin.loc_frame)

    def populate(self, sf):
        Label(sf.frame, text='Tag Options', anchor='w').grid(row=0, column=0, sticky='ew')
        # frame = Frame(sf.frame, bg='blue').grid(row=0, column=0)
        self.cwin.loc_frame.type_frame = Frame(sf.frame)
        self.cwin.loc_frame.type_frame.grid(row=1, column=0, sticky='ew')
        Label(sf.frame, text='Attribute Options', anchor='w').grid(row=2, column=0, sticky='ew')
        self.cwin.loc_frame.attr_frame = Frame(sf.frame)
        self.cwin.loc_frame.attr_frame.grid(row=3, column=0, sticky='ew')
        # '''Put in some fake data'''
        # for row in range(0, 100):
        #     Label(sf.frame, text="%s" % row, width=3, borderwidth="1",
        #           relief="solid").grid(row=row, column=0)
        #     t="this is the second column for row %s" %row
        #     Label(sf.frame, text=t).grid(row=row, column=1)

    def mouse_btn(self, event):
        # print "mouse event (%s, %s)" % (event.type, event.num)
        if (event.type, event.num) == ('4', 1):
            x = self.descale(event.x)
            y = self.descale(event.y)
            # print "mouse click at (%s, %s)" % (x, y)
            self.show_locator_options(x, y)

    def show_locator_options(self, x, y):
        # clicking on an outlined element in the browser image should correlate (by position) with at least one
        # of self.processor_elems, but possibly more. When multiple css types ("input", "a", "button", etc.) are
        # matched, use radiobuttons to choose the desired css options
        for child in self.cwin.loc_frame.type_frame.winfo_children():
            child.grid_forget()
        default = None
        for (i, key) in enumerate(self.processor_elems):
            self.clicked_elems[key] = filter(self.point_in_elem_outline(x, y), self.processor_elems[key])
            if len(self.clicked_elems[key]):
                print "clicked %d %s elements" % (len(self.clicked_elems[key]), key)
            if len(self.clicked_elems[key]) == 1:
                # print "geom = %s" % self.clicked_elems[key][0]['geom']
                rb = Radiobutton(self.cwin.loc_frame.type_frame, text=key, variable=self.locator_css_type, value=key,
                                 command=self.show_radio_btn)
                rb.grid(row=0, column=i)
                if default is None:
                    default = key
                    rb.select()
                    rb.invoke()
                    # self.locator_css_type.set(default)
                    # self.show_radio_btn()

    def show_radio_btn(self):
        key = self.locator_css_type.get()
        print "radiobutton value %s" % key
        elem = self.clicked_elems[key][0]
        self.locator_part_cbs = []
        frame = self.cwin.loc_frame.attr_frame
        for child in frame.winfo_children():
            child.grid_forget()
        ai = AutoIncrementer()
        if len(elem['partial_values']) > 0:
            Label(frame, text='(matches) Partial Values:').grid(row=ai.row, column=0, sticky='w')
            for p_attr in elem['partial_values']:
                matches = "(%d)" % p_attr['matches']
                cb_val = p_attr['selector']
                cb_text = "%4s %s%s" % (matches, elem['tag'], cb_val)
                intvar = IntVar()
                cb = Checkbutton(self.cwin.loc_frame.attr_frame, variable=intvar, text=cb_text,
                                 command=lambda: self.set_locator_part(elem['tag']))
                cb.grid(row=ai.row, column=0, sticky='w')
                self.locator_part_cbs.append({'cb': cb, 'var': intvar, 'val': cb_val})
        Label(frame, text='Complete css locator:').grid(row=ai.row, column=0, sticky='w')
        intvar = IntVar()
        cb = Checkbutton(self.cwin.loc_frame.attr_frame, variable = intvar, text=elem['value'],
                         command=self.set_locator_full)
        cb.grid(row=ai.row, column=0, sticky='w')
        self.locator_full_cb = {'cb': cb, 'var': intvar, 'val': elem['value']}
        if elem['text'] is not None:
            intvar = IntVar()
            Label(frame, text='Required text:').grid(row=ai.row, column=0, sticky='w')
            cb = Checkbutton(self.cwin.loc_frame.attr_frame, variable = intvar, text=elem['text'],
                             command=self.set_locator_text)
            cb.grid(row=ai.row, column=0, sticky='w')
            self.locator_text_cb = {'cb': cb, 'var': intvar, 'val': elem['text']}

    def set_locator_text(self):
        if self.locator_text_cb['var'].get():
            self.locator_req_text.set(1)
            self.locator_text_val.set(self.locator_text_cb['val'])
        else:
            self.locator_req_text.set(0)
            self.locator_text_val.set('')

    def set_locator_part(self, tag):
        self.locator_full_cb['var'].set(0)
        attrs = []
        for cb in self.locator_part_cbs:
            if cb['var'].get():
                attrs.append(cb['val'])
        self.find_by_var.set('css selector')
        self.find_value_var.set("%s%s" % (tag, ''.join(attrs)))

    def set_locator_full(self):
        if self.locator_full_cb['var'].get():
            for cb in self.locator_part_cbs:
                cb['var'].set(0)
            self.find_by_var.set('css selector')
            self.find_value_var.set(self.locator_full_cb['val'])

    def on_canvas_closing(self):
        self.im_canvas = None
        self.cwin.destroy()

    def scale(self, dim):
        return dim * self.cwin.scale + self.cwin.canvas_borderwidth

    def descale(self, dim):
        return (dim - self.cwin.canvas_borderwidth) / self.cwin.scale

    def point_in_elem_outline(self, x, y):

        def fn(elem):
            x1 = elem["geom"]["x1"]
            y1 = elem["geom"]["y1"]
            y2 = elem["geom"]["y2"]
            x2 = elem["geom"]["x2"]
            return x1 <= int(x) <= x2  and y1 <= int(y) <= y2

        return fn

    def draw_outlines(self, elems, color='red', clear=True, width=2):
        if self.im_canvas is not None:
            if clear:
                while len(self.polygons):
                    self.im_canvas.delete(self.polygons.pop())
            for elem in elems:
                # print "%s[%s]: creating polygon from geom: (%s, %s), (%s, %s)" % (
                #     elem["tag"], elem["index"], elem["geom"]["x1"], elem["geom"]["y1"], elem["geom"]["x2"],
                #     elem["geom"]["y2"])
                x1 = self.scale(elem["geom"]["x1"]) + (width / 2.0)
                y1 = self.scale(elem["geom"]["y1"]) + (width / 2.0)
                y2 = self.scale(elem["geom"]["y2"]) - (width / 2.0)
                x2 = self.scale(elem["geom"]["x2"]) - (width / 2.0)
                self.polygons.append(self.im_canvas.create_polygon(x1, y1, x1, y2, x2, y2, x2, y1, outline=color,
                                                                   fill='', width=width))


def run_web_inspector(cfg):
    root = Tk()
    root.wm_title("eConsole test utility")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    # preferred place to set these values is in <runtime directory>.web_inspector_config.yml
    gui_cfg = {
        'tmp_dir': cfg.get('tmp_dir', './tmp'),
        'log_window_height': cfg.get('log_window_height', 20),
        'rec_window_height': cfg.get('rec_window_height', 5),
        'screenshot_dir': cfg.get('screenshot_dir', '.')
    }
    try:
        os.makedirs(gui_cfg['tmp_dir'])
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(cfg['tmp_dir']):
            pass
        else:
            raise

    _app = Inspector(root, gui_cfg)
    _app.mainloop()
