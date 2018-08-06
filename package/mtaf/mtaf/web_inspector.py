import os
from time import sleep, time
from user_exception import UserException as Ux
import mtaf_logging
from angular_actions import AngularActions
import threading
import json
from filters import get_filter
import errno
from time import strftime, localtime
import six
from mtaf.trace import Trace
from eConsole import views
import shutil
if six.PY3:
    from tkinter import filedialog
    from tkinter import *
    from tkinter import simpledialog as tk_simple_dialog
    from tkinter.ttk import Combobox
    from queue import Queue
else:
    from Tkinter import *
    import tkfilebrowser
    import tk_simple_dialog
    from ttk import Combobox
    from Queue import Queue


angular_actions = AngularActions()
mtaf_logging.disable_console()
log = mtaf_logging.get_logger('mtaf.inspector')
re_dumpsys = re.compile('(?ms).*mCurrentFocus=\S+\s+\S+\s+([^/]+)/([^}]+)')
btn_default_bg = '#d9d9d9'
btn_select_bg = '#d97979'


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
        # six.print_("AutoIncrementer returning %s for name %s" % (prev_count, name))
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


class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """
    def __init__(self, parent, *_args):
        Frame.__init__(self, parent, *_args)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)

        self.rowconfigure(0, weight=1)
        vscrollbar.grid(sticky='ns', row=0, column=1)

        canvas = Canvas(self, bd=0, highlightthickness=0, yscrollcommand=vscrollbar.set)

        canvas.grid(sticky='nsew', row=0, column=0)

        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior, anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
            if interior.winfo_reqheight() != canvas.winfo_height():
                # update the canvas's height to fit the inner frame
                canvas.config(height=interior.winfo_reqheight())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)


class ScrolledLogwin(Frame):
    def __init__(self, parent, height=20, label=None):
        Frame.__init__(self, parent)
        self.log_q = Queue()
        self.parent = parent
        row = 0
        if label is not None:
            self.label = Label(self, text=label)
            self.label.grid(row=row, column=0, columnspan=2, sticky='ew')
            row += 1
        self.txt = Text(self, height=height)
        self.scrollback = 5000
        self.txt.configure(state=DISABLED)
        self.sb = Scrollbar(self, command=self.txt.yview)
        self.txt["yscrollcommand"] = self.sb.set
        self.txt.grid(row=row, column=0, sticky='nsew', padx=2, pady=2)
        self.sb.grid(row=row, column=1, sticky='ns', padx=2, pady=2)
        self.rowconfigure(row, weight=1)
        self.print_buf = ''
        self.read_q()

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
        self.automation_name = None
        self.clickable_element = None
        self.cwin = None
        self.cwin_x = None
        self.cwin_y = None
        self.devices = []
        self.elem_index = None
        self.elem_indices = []
        self.elems = []
        self.elems_btns = []
        self.exec_text = StringVar()
        self.find_button = None
        self.find_by_var = None
        self.find_value_var = None
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
        self.locator_by_values = ['id', 'xpath', 'link text',"partial link text", "name", "tag name", "class name",
                                  "css selector"]
        self.locators = {}
        self.log_frame = None
        self.menu = None
        self.new_drag_polygon_x1 = None
        self.new_drag_polygon_y1 = None
        self.parent_element = None
        self.polygons = []
        self.script_btn_enable_states = {}
        self.script_fd = None
        self.script_file = StringVar()
        self.script_file.set(os.path.join(self.cfg['tmp_dir'], 'web_inspector_scripts', 'web_inspector_script.txt'))
        self.script_recording = False
        self.script_rec_btns = []
        self.script_running = False
        self.script_run_btns = []
        self.script_state = 'stopped'
        self.rec_file = os.path.join(self.cfg['tmp_dir'], 'web_inspector_recording.txt')
        self.loc_file = os.path.join(self.cfg['tmp_dir'], 'web_inspector_locators.json')
        self.rec_frame = None
        self.swipe_ms_var = StringVar()
        self.swipe_y1_var = StringVar()
        self.swipe_y2_var = StringVar()
        self.tap_x_var = StringVar()
        self.tap_y_var = StringVar()
        self.text_to_send = None
        self.top_frames = []
        self.use_parent = None
        self.views = {key[:-5]: val for (key, val) in views.__dict__.items() if key[-5:] == '_view'}
        self.within_frame = None
        self.worker_thread = None
        self.zpath_frame_btns = {}
        self.zpath_frame = None
        self.zpath_label = None
        self.zpaths = None

        try:
            with open(self.loc_file, 'r') as f:
                self.locators = json.loads(f.read())
        except (IOError, ValueError):
            pass

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
            'Close Browser': lambda: self.do_cmd(self.close_browser)
        }
        self.create_menus(parent)

    def open_browser(self):
        six.print_("Opening Browser...", end='')
        self.record("self.open_browser()")
        self.views['base'].open_browser()
        self.browser_is_open = True
        url = "http://staging-econsole.esihs.net"
        self.record("self.views['base'].get_url('%s')" % url)
        self.views['base'].get_url(url)
        self.menu.enable_items(self.browser_is_open)
        self.elems = []
        six.print_("Done")

    def close_browser(self):
        six.print_("Closing Browser...", end='')
        self.record("self.close_browser()")
        self.views['base'].close_browser()
        self.browser_is_open = False
        self.menu.enable_items(self.browser_is_open)
        self.elems = []
        six.print_("Done")

    def get_title(self):
        self.record("self.get_title()")
        six.print_(angular_actions.driver.title)

    def get_current_url(self):
        self.record("self.current_url()")
        six.print_(angular_actions.driver.current_url)

    def populate_top_frames(self):
        top_frame_row = 0
        for top_frame in self.top_frames:
            if hasattr(top_frame, 'expand_y') and top_frame.expand_y is True:
                self.grid_rowconfigure(top_frame_row, weight=1)
            top_frame.grid_forget()
            top_frame.grid(row=top_frame_row, column=0, padx=4, pady=2, sticky='news')
            top_frame_row += 1

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
        filename = tkfilebrowser.askopenfilename(initialdir=os.path.join(self.cfg['tmp_dir'], 'web_inspector_scripts'),
                                                 initialfile=os.path.basename(self.script_file.get()),
                                                 title="Select script to print",
                                                 filetypes=(
                                                     (".txt files", "*.txt"),
                                                     ("all files", "*.*"))
                                                 )
        if filename:
            self.script_file.set(filename)
            six.print_('>> Printing contents of %s:' % self.script_file.get())
            try:
                with open(self.script_file.get(), 'r') as f:
                    for line in f:
                        six.print_(line, end="")
            except BaseException as e:
                six.print_('got exception: %s' % e)
            six.print_('>> Done')
        self.update_script_state('stopped')

    def run_script(self):
        self.update_script_state('running')
        filename = tkfilebrowser.askopenfilename(initialdir=os.path.join(self.cfg['tmp_dir'], 'web_inspector_scripts'),
                                                 initialfile=os.path.basename(self.script_file.get()),
                                                 title="Select script to run",
                                                 filetypes=(
                                                     (".txt files", "*.txt"),
                                                     ("all files", "*.*"))
                                                 )
        if filename:
            self.disable_buttons()
            self.update_idletasks()
            self.script_running = True
            self.script_file.set(filename)
            six.print_(">> Running script file %s" % self.script_file.get())
            try:
                with open(self.script_file.get(), 'r') as f:
                    try:
                        for line in f:
                            line = line.strip()
                            if line[0] == '#' or line[0] == '"':
                                continue
                            if not self.script_running:
                                break
                            six.print_("exec: %s" % line.strip())
                            six.exec_(line.strip())
                    except Exception as _e:
                        six.print_("exec raised exception: %s" % _e)
            except BaseException as e:
                six.print_("open(%s, 'r') got exception: %s" % e)
            self.script_running = False
            self.enable_buttons()
            six.print_(">> Done")
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
            six.print_(">> Recording script file %s" % self.script_file.get())
            self.script_fd = open(self.script_file.get(), 'w')
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
            six.print_(">> Recording to end of script file %s" % self.script_file.get(), end='')
            self.script_fd = open(self.script_file.get(), 'a')
        else:
            self.update_script_state('stopped')

    def copy_script(self):
        self.update_script_state('recording')
        filename = tkfilebrowser.asksaveasfilename(initialdir=os.path.join(self.cfg['tmp_dir'], 'web_inspector_scripts'),
                                                   initialfile=os.path.basename(self.script_file.get()),
                                                   title="Copy current script to file: ",
                                                   filetypes=(
                                                       (".txt files", "*.txt"),
                                                       ("all files", "*.*"))
                                                   )
        if filename:
            if filename == self.script_file.get():
                six.print_("not copying %s to same filename")
            else:
                six.print_("copying %s to %s... " % (self.script_file.get(), filename), end='')
                shutil.copyfile(self.script_file.get(), filename)
                self.script_file.set(filename)
                six.print_("Done")
        self.update_script_state('stopped')

    def stop_script(self):
        # if running, stop executing script lines
        self.script_running = False
        # if recording or adding, stop
        if self.script_fd is not None:
            self.script_fd.close()
            self.script_fd = None
        self.update_script_state('stopped')
        six.print_(">> Done")

    def record(self, txt):
        self.rec_frame.write(txt + '\n')
        if self.script_fd is not None:
            self.script_fd.write(txt + '\n')
        timestamp = strftime('%m_%d_%y-%H_%M_%S', localtime())
        with open(self.rec_file, 'a') as f:
            f.write('%s %s\n' % (timestamp, txt.encode('utf-8')))

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
            log.debug("worker thread done: %s" % self.worker_thread.name)
            self.worker_thread = None
            # if do_cmd thread is done, re-enable the menubar dropdowns
            self.enable_buttons()

    def enable_buttons(self):
        for i in range(len(self.menu.items)):
            self.menu.entryconfig(i + 1, state=NORMAL)
        if self.browser_is_open:
            for btn in self.browser_btns:
                btn.configure(state=NORMAL)
        if len(self.elems):
            for btn in self.elems_btns:
                btn.configure(state=NORMAL)
        # depending on self.browser_is_enabled value, enable/disable dropdown menu items
        self.menu.enable_items(self.browser_is_open)

    def update_script_state(self, state):
        self.script_state = state
        for btn in self.script_btn_enable_states:
            if state in self.script_btn_enable_states[btn]:
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
        bottom_frame.script_frame.record_script = btn
        self.script_btn_enable_states[btn] = "stopped"

        btn = Button(bottom_frame.script_frame, text="Stop Recording", bg=btn_default_bg, command=self.stop_script,
                     state=DISABLED)
        btn.grid(row=1, column=ai.col, sticky='ew', padx=4, pady=2)
        bottom_frame.script_frame.stop_script = btn
        self.script_btn_enable_states[btn] = "recording"

        btn = Button(bottom_frame.script_frame, text="Print", bg=btn_default_bg, command=self.print_script)
        btn.grid(row=1, column=ai.col, sticky='ew', padx=4, pady=2)
        bottom_frame.script_frame.print_script = btn
        self.script_btn_enable_states[btn] = "stopped"

        btn = Button(bottom_frame.script_frame, text="Run", bg=btn_default_bg, command=self.run_script)
        btn.grid(row=1, column=ai.col, sticky='ew', padx=4, pady=2)
        bottom_frame.script_frame.run_script = btn
        self.script_btn_enable_states[btn] = "stopped"

        btn = Button(bottom_frame.script_frame, text="Add to Script", bg=btn_default_bg, command=self.add_to_script)
        btn.grid(row=1, column=ai.col, sticky='ew', padx=4, pady=2)
        bottom_frame.script_frame.add_to_script = btn
        self.script_btn_enable_states[btn] = "stopped"

        btn = Button(bottom_frame.script_frame, text="Copy", bg=btn_default_bg, command=self.copy_script)
        btn.grid(row=1, column=ai.col, sticky='ew', padx=4, pady=2)
        bottom_frame.script_frame.copy_script = btn
        self.script_btn_enable_states[btn] = "stopped"

        btn = Button(bottom_frame.script_frame, text="Change Current", bg=btn_default_bg, command=self.change_script)
        btn.grid(row=1, column=ai.col, sticky='ew', padx=4, pady=2)
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
        self.log_frame = ScrolledLogwin(pw, height=self.cfg['log_window_height'], label='standard output')
        self.log_frame.grid_columnconfigure(0, weight=1)
        pw.add(self.log_frame, stretch='always')
        rec_frame = ScrolledLogwin(pw, height=self.cfg['log_window_height'], label='recorded text')
        self.rec_frame = rec_frame
        rec_frame.grid_columnconfigure(0, weight=1)
        pw.add(rec_frame, stretch='always')
        pw.expand_y = True
        return pw

    @staticmethod
    def defocus(event):
        event.widget.selection_clear()

    def create_exec_frame(self):
        exec_frame = Frame(self, bg="brown")
        exec_frame.btn = Button(exec_frame, text="exec:", command=lambda: self.do_cmd(self.exec_code),
                                bg=btn_default_bg, state=NORMAL)
        exec_frame.btn.grid(row=0, column=0)
        exec_frame.entry = Entry(exec_frame, textvariable=self.exec_text)
        exec_frame.entry.grid(row=0, column=1, sticky='news')
        exec_frame.columnconfigure(1, weight=1)
        # exec_frame.grid(row=self.top_frame_row, column=0, padx=4, pady=4, sticky='news')
        # self.top_frame_row += 1
        return exec_frame

    def exec_code(self):
        text = self.exec_text.get()
        try:
            six.exec_(text)
        except Exception as _e:
            six.print_("exec raised exception: %s" % _e)

    def callback(self, *_args):
        self.find_button.configure(bg=btn_select_bg, activebackground=btn_select_bg)

    def create_btn_frame(self):
        ai = AutoIncrementer()
        btn_frame = ButtonFrame(self, bg="brown")

        btn_frame.find_frame = Frame(btn_frame, bg='tan')
        btn_frame.find_frame.grid(row=ai.bf_row, column=0, sticky='ew', padx=2, pady=2)
        btn = Button(btn_frame.find_frame, text="find elements:", bg=btn_default_bg,
                     command=lambda: self.do_cmd(self.find_elements), state=DISABLED)
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
        btn_frame.find_frame.loc.grid_columnconfigure(0, weight=1)
        loc_column = ai.ffr
        btn_frame.find_frame.loc.grid(row=0, column=loc_column, padx=2, pady=2, sticky='new')
        btn_frame.find_frame.grid_columnconfigure(loc_column, weight=1)

        self.use_parent = IntVar()
        self.use_parent.set(0)
        btn_frame.find_frame.cbs.use_parent = Checkbutton(btn_frame.find_frame.cbs, text='from Parent',
                                                          variable=self.use_parent, state=DISABLED)
        btn_frame.find_frame.cbs.use_parent.grid(row=0, column=0, padx=2, pady=2, sticky='ew')

        self.within_frame = IntVar()
        self.within_frame.set(0)
        btn_frame.find_frame.cbs.within_frame = Checkbutton(btn_frame.find_frame.cbs, text='within frame',
                                                        variable=self.within_frame, state=DISABLED)
        btn_frame.find_frame.cbs.within_frame.grid(row=1, column=0, padx=2, pady=2, sticky='ew')

        self.find_value_var = StringVar()
        self.find_value_var.trace('w', self.callback)
        btn_frame.find_frame.loc.value = Combobox(btn_frame.find_frame.loc, width=60,
                                                  values=self.get_filtered_locator_keys(),
                                                  textvariable=self.find_value_var)
        self.browser_btns.append(btn_frame.find_frame.loc.value)
        btn_frame.find_frame.loc.value.bind('<<ComboboxSelected>>', self.update_find_frame)
        btn_frame.find_frame.loc.value.bind("<FocusIn>", self.defocus)
        btn_frame.find_frame.loc.hsb = Scrollbar(btn_frame.find_frame.loc, orient=HORIZONTAL,
                                                 command=btn_frame.find_frame.loc.value.xview)
        btn_frame.find_frame.loc.value["xscrollcommand"] = btn_frame.find_frame.loc.hsb.set
        btn_frame.find_frame.loc.value.grid(row=0, column=0, padx=2, pady=0, sticky='ew')
        btn_frame.find_frame.loc.hsb.grid(row=1, column=0, sticky='ew')

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
            'Brower Actions': [
                {'label': 'Get Current Page Title', 'uses_browser': True},
                {'label': 'Get Current URL', 'uses_browser': True},
            ],
            'Browser Session': [
                {'label':'Open Browser', 'uses_browser': False},
                {'label':'Close Browser', 'uses_browser': True}
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
        self.quit()

    def do_cmd(self, cmd):
        if self.worker_thread is not None:
            six.print_("worker thread busy: %s" % cmd.__name__)
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

    def update_find_widgets(self, event):
        find_by = self.find_by_var.get()
        if (find_by == 'id') and self.parent_element is not None:
            self.btn_frame.find_frame.cbs.use_parent.configure(state=NORMAL)
        else:
            self.btn_frame.find_frame.cbs.use_parent.configure(state=DISABLED)
            self.use_parent.set(0)
        if find_by[-11:] == 'locator_all' and self.frame_element is not None:
            self.btn_frame.find_frame.cbs.within_frame.configure(state=NORMAL)
        else:
            self.btn_frame.find_frame.cbs.within_frame.configure(state=DISABLED)

    def find_elements_by_locator_name(self, locator):
        by = locator['by']
        value = locator['value']
        elems = []
        try:
            if by[-3:] == 'all':
                view_name = by[:-12]
                # self.record("finding elements in view %s using locator %s" % (view_name, value))
                elems = getattr(self.views[view_name].all, value)
            else:
                view_name = by[:-8]
                # self.record("finding elements in view %s using locator %s" % (view_name, value))
                elems = [getattr(self.views[view_name], value)]
        except Ux as _e:
            six.print_(_e.message)
        if self.within_frame.get():
            return filter(get_filter('within_frame', frame=self.frame_element), elems)
        else:
            if elems == [None]:
                return []
            return elems

    def find_elements_with_driver(self, locator):
        angular_actions.wait_until_page_ready()
        by = locator['by']
        value = locator['value']
        if self.use_parent.get():
            return self.parent_element.find_elements(by, value)
        else:
            return angular_actions.driver.find_elements(by, value)

    def get_filtered_locator_keys(self):
        sorted_keys = sorted(self.locators.keys(), key=lambda x: self.locators[x]['time'], reverse=True)
        filtered_keys = filter(lambda x: self.locators[x]['by'] in self.locator_by_values, sorted_keys)
        return ["%s:%s" % (self.locators[key]['by'], key) for key in filtered_keys]

    def update_locator_list(self, locator=None):
        self.btn_frame.find_frame.by.configure(values=self.locator_by_values)
        # - find_elements passes in a locator value, which is added to self.locators
        # - a plugin that adds values to self.locator_by_values will need to call this method with no locator argument
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

    def find_elements(self):
        six.print_("finding elements...", end='')
        self.find_button.configure(bg=btn_default_bg)
        locator = {
            'by': self.find_by_var.get(),
            'value': self.find_value_var.get(),
            'use_parent': bool(self.use_parent.get())
        }
        self.update_locator_list(locator)
        self.find_elements_by_locator(locator)

    def find_elements_by_locator(self, locator):
        self.record("self.find_elements_by_locator(%s)" % locator)
        if locator['by'][-7:] == 'locator' or locator['by'][-11:] == 'locator_all':
            self.elems = self.find_elements_by_locator_name(locator)
        else:
            self.elems = self.find_elements_with_driver(locator)
            # keep frame element setting if using "by" value ending in '*_locator'
            self.frame_element = None
            self.within_frame.set(0)
        _msg = "%s element%s found" % (len(self.elems), '' if len(self.elems) == 1 else 's')
        six.print_(_msg)
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
        self.record('getting element %d attributes' % index)
        elem = self.elems[index]
        script = 'var items = {};' \
            + 'for (index = 0; index < arguments[0].attributes.length; ++index) ' \
            + '{ items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value };' \
            + 'return items;'
        attrs = angular_actions.driver.execute_script(script, elem)
        six.print_("\nattributes for element %d:" % index)
        for key in attrs.keys():
            six.print_("%s: %s" % (key, attrs[key]))

    def click_element(self):
        text_index = self.elem_index.get()
        if text_index == '':
            return
        index = int(text_index)
        self.click_element_by_index(index)

    def click_element_by_index(self, index):
        self.record('self.click_element_by_index(%s)' % index)
        self.elems[index].click()

    def clear_element(self):
        text_index = self.elem_index.get()
        if text_index == '':
            return
        index = int(text_index)
        self.record('clearing element %d' % index)
        self.elems[index].clear()

    def set_parent(self):
        text_index = self.elem_index.get()
        if text_index == '':
            return
        index = int(text_index)
        self.record('setting element %d as parent' % index)
        self.parent_element = self.elems[index]
        self.update_find_widgets(None)

    def set_frame(self):
        text_index = self.elem_index.get()
        if text_index == '':
            return
        index = int(text_index)
        self.record('setting element %d as frame' % index)
        self.frame_element = self.elems[index]
        self.update_find_widgets(None)

    def input_text(self):
        text_index = self.elem_index.get()
        if text_index == '':
            return
        index = int(text_index)
        text = self.text_to_send.get()
        self.input_text_to_element_index(text, index)

    def input_text_to_element_index(self, text, index):
        self.record("self.input_text_to_element_index('%s', %d)" % (text, index))
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
            six.print_("got exception %s" % _e)
        self.update_find_widgets(None)

    def input_enter(self):
        text_index = self.elem_index.get()
        if text_index == '':
            return
        index = int(text_index)
        self.record('sending \\n to element %d' % index)
        try:
            self.elems[index].send_keys('\n')
        except BaseException as _e:
            six.print_("got exception %s" % _e)
        self.update_find_widgets(None)

    @staticmethod
    def log_action(spud_serial, action):
        (reply, elapsed, groups) = spud_serial.do_action(action)
        lines = reply.split('\n')
        log.debug('cmd: %s\nelapsed: [%5.3f s]  \necho: "%s"\n' %
                  (action['cmd'], elapsed, repr(lines[0].encode('string_escape'))))
        for line in lines[1:]:
            log.debug(' '*7 + line.encode('string_escape'))


def run_web_inspector(cfg):
    root = Tk()
    root.wm_title("eConsole test utility")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    gui_cfg = {
        'tmp_dir': cfg.get('tmp_dir', './tmp'),
        'log_window_height': cfg.get('log_window_height', 20)
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
