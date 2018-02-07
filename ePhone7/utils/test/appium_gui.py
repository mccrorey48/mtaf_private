import os
from Tkinter import *
from ttk import Combobox
from time import sleep, time
from lib.user_exception import UserException as Ux
from pyand import ADB
import lib.logging_esi as logging
from lib.android import expand_zpath
from selenium.common.exceptions import NoSuchElementException, InvalidSelectorException
import threading
import json
from lib.filters import get_filter
from PIL import Image, ImageTk

uut = 'ePhone7'

if uut == 'ePhone7':
    from ePhone7.config.configure import cfg
    from ePhone7.views import *
    from ePhone7.utils.get_softphone import get_softphone
    from ePhone7.views.base_view import keycodes
    from ePhone7.utils.csv.xml_to_csv import xml_to_csv
    from ePhone7.utils.csv.parse_ids import parse_ids, parse_zpaths
    from ePhone7.utils.spud_serial import SpudSerial
    from ePhone7.utils.usb_enable import usb_enable
    from ePhone7.utils.get_focused_app import get_focused_app
    from ePhone7.utils.versions import *

log = logging.get_logger('esi.appium_gui')


class Command(object):
    def __init__(self, label, action):
        self.label = label
        self.action = action


class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args)

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
        log.debug("write: _txt = [%s], len=%d" % (repr(_txt), len(_txt)))
        if len(_txt) > 0 and _txt[-1] == '\n':
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
        # self.delete('0.0', 'end - %d lines' % self.scrollback)
        self.see('end')
        self.update_idletasks()
        self.configure(state=DISABLED)


class LogFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg='brown')
        print "parent = " + repr(parent)
        self.txt = ScrolledLogwin(self, width=80, height=20, name='cmd')
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


class MyMenu(Menu):

    def __init__(self, parent, *args, **kwargs):
        Menu.__init__(self, parent, *args, **kwargs)
        self.appium_sub_menu = None
        self.appium_sub_menu_max_index = None
        self.other_sub_menu = None
        self.other_sub_menu_max_index = None


class AttrFrame(Frame):
    index = None


class BottomFrame(Frame):
    mk_canvas = None


class ButtonFrame(Frame):
    find_frame = None


class TestGui(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent, bg="brown")
        self.appium_is_open = False
        self.attr_frame = None
        self.cwin = None
        self.drag_polygon = None
        self.drag_polygon_x1 = None
        self.drag_polygon_y1 = None
        self.drag_polygon_x2 = None
        self.drag_polygon_y2 = None
        self.elem_index = None
        self.find_by_var = None
        self.find_value_var = None
        self.frame_element = None
        self.id_frame = None
        self.id_frame_btns = {}
        self.id_label = None
        self.ids = None
        self.ids = None
        self.im_canvas = None
        self.im_width = None
        self.im_height = None
        self.keycode_name = None
        self.parent_element = None
        self.use_parent = None
        self.worker_thread = None
        self.zpath_frame = None
        self.zpath_frame_btns = {}
        self.zpath_label = None
        self.zpaths = None
        self.appium_btns = []
        self.appium_commands = []
        self.elem_indices = []
        self.elems = []
        self.no_appium_btns = []
        self.other_commands = []
        self.polygons = []
        self.locators = {"Coworkers": {"by": "uia_text", "use_parent": 0, "time": ""}}
        self.views = {'contacts': contacts_view, 'history': history_view, 'voicemail': voicemail_view, 'dial': dial_view,
                      'prefs': prefs_view}
        self.within_frame = IntVar()
        self.tap_y_var = StringVar()
        self.tap_x_var = StringVar()
        self.swipe_y1_var = StringVar()
        self.swipe_y2_var = StringVar()
        self.swipe_ms_var = StringVar()
        self.exec_text = StringVar()

        try:
            with open('tmp/appium_gui_locators.json', 'r') as f:
                self.locators = json.loads(f.read())
        except IOError:
            pass

        self.create_commands()
        self.menu = self.create_menus(parent)
        self.top_frame_row = 0
        self.btn_frame = self.create_btn_frame()
        self.softphone_frame = self.create_softphone_frame()
        self.exec_frame = self.create_exec_frame()
        self.log_frame = self.create_log_frame()
        self.bottom_frame = self.create_bottom_frame()
        self.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, padx=2, pady=2, sticky='nsew')
        for btn in self.appium_btns:
            btn.configure(state=DISABLED)
        for i in range(self.menu.appium_sub_menu_max_index):
            self.menu.appium_sub_menu.entryconfig(i + 1, state=DISABLED)
        for btn in self.no_appium_btns:
            btn.configure(state=NORMAL)
        for i in range(self.menu.other_sub_menu_max_index):
            self.menu.other_sub_menu.entryconfig(i + 1, state=NORMAL)

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
            log.debug("worker thread died")
            self.worker_thread = None
            self.menu.entryconfig(3, state=NORMAL)
            self.menu.entryconfig(4, state=NORMAL)
            if self.appium_is_open:
                self.menu.entryconfig(1, state=NORMAL)
                self.menu.entryconfig(2, state=DISABLED)
                self.menu.entryconfig(3, label='Stop Appium', command=lambda: self.do_cmd(self.close_appium))
                for btn in self.appium_btns:
                    btn.configure(state=NORMAL)
                for i in range(self.menu.appium_sub_menu_max_index):
                    self.menu.appium_sub_menu.entryconfig(i + 1, state=NORMAL)
                for btn in self.no_appium_btns:
                    btn.configure(state=DISABLED)
                for i in range(self.menu.other_sub_menu_max_index):
                    self.menu.other_sub_menu.entryconfig(i + 1, state=DISABLED)
            else:
                self.menu.entryconfig(1, state=DISABLED)
                self.menu.entryconfig(2, state=NORMAL)
                self.menu.entryconfig(3, label='Start Appium', command=lambda: self.do_cmd(self.open_appium))
                for btn in self.appium_btns:
                    btn.configure(state=DISABLED)
                for i in range(self.menu.appium_sub_menu_max_index):
                    self.menu.appium_sub_menu.entryconfig(i + 1, state=DISABLED)
                for btn in self.no_appium_btns:
                    btn.configure(state=NORMAL)
                for i in range(self.menu.other_sub_menu_max_index):
                    self.menu.other_sub_menu.entryconfig(i + 1, state=NORMAL)

    def create_bottom_frame(self):
        bottom_frame = BottomFrame(self, bg="tan")
        bottom_frame.grid_columnconfigure(0, weight=1)
        bottom_frame.mk_canvas = Button(bottom_frame, text="screenshot", command=self.create_cwin)
        bottom_frame.mk_canvas.grid(row=0, column=0, sticky='e', padx=2, pady=2)
        # self.appium_btns.append(bottom_frame.mk_canvas)
        bottom_frame.Quit = Button(bottom_frame, text="Quit", command=self.close_appium_and_quit)
        bottom_frame.Quit.grid(row=0, column=1, sticky='e', padx=2, pady=2)
        bottom_frame.grid(row=self.top_frame_row, column=0, padx=4, pady=4, sticky='news')
        self.top_frame_row += 1
        return bottom_frame

    def elem_selected(self, elems):
        if self.drag_polygon is None:
            return True
        dx1 = min(self.drag_polygon_x1, self.drag_polygon_x2)
        dx2 = max(self.drag_polygon_x1, self.drag_polygon_x2)
        dy1 = min(self.drag_polygon_y1, self.drag_polygon_y2)
        dy2 = max(self.drag_polygon_y1, self.drag_polygon_y2)
        for elem in elems:
            x1 = int(elem['x1']) * self.cwin.scale
            x2 = int(elem['x2']) * self.cwin.scale
            y1 = int(elem['y1']) * self.cwin.scale
            y2 = int(elem['y2']) * self.cwin.scale
            if x1 >= dx1 and x2 <= dx2 and y1 >= dy1 and y2 <= dy2:
                return True
        # print "(%s,%s) -> (%s,%s) not in (%s,%s) -> (%s,%s)" % (x1, y1, x2, y2, dx1, dy1, dx2, dy2)
        return False

    def show_zpaths(self):
        pass

    def create_cwin(self):
        self.bottom_frame.mk_canvas.configure(state=DISABLED)
        if self.appium_is_open:
            self.get_screenshot()
            self.get_xml()
        x = self.winfo_rootx()
        y = self.winfo_rooty()
        w = self.winfo_width()
        if self.cwin is not None:
            self.destroy_loc_frames()
            self.cwin.destroy()
            self.cwin = None
        self.update_idletasks()
        self.cwin = Toplevel(root, bg='cyan')
        self.cwin.protocol("WM_DELETE_WINDOW", self.on_canvas_closing)
        self.cwin.resizable(width=False, height=True)
        self.cwin.geometry("+%d+%d" % (x + w + 20, y - 70))
        self.cwin.scale = 0.5
        self.im_width = int(600 * self.cwin.scale)
        self.im_height = int(1024 * self.cwin.scale)
        self.cwin.minsize(width=self.im_width, height=self.im_height)
        self.im_canvas = Canvas(self.cwin, height=self.im_height, width=self.im_width, bg='darkgray')
        fullpath = os.path.join(cfg.test_screenshot_folder, 'appium_gui.png')
        self.im_canvas.im = Image.open(fullpath)
        small = self.im_canvas.im.resize((self.im_width, self.im_height))
        self.im_canvas.photo = ImageTk.PhotoImage(small)
        self.im_canvas.create_image(self.im_width/2, self.im_height/2, image=self.im_canvas.photo)
        # self.im_canvas.grid(column=0, row=0, rowspan=2)
        self.im_canvas.grid(column=0, row=0)
        self.im_canvas.bind('<Button-1>', self.mouse_btn)
        self.im_canvas.bind('<Button-2>', self.mouse_btn)
        self.im_canvas.bind('<Button-3>', self.mouse_btn)
        self.im_canvas.bind('<B1-Motion>', self.mouse_btn)
        self.im_canvas.bind('<ButtonRelease-1>', self.mouse_btn)
        self.cwin.rowconfigure(0, weight=1)
        self.create_loc_frames()
        self.bottom_frame.mk_canvas.configure(state=NORMAL)

    def update_loc_frames(self):
        self.destroy_loc_frames()
        self.create_loc_frames()

    def destroy_loc_frames(self):
        if self.id_frame is not None:
            for _id in self.id_frame_btns:
                self.id_frame_btns[_id].grid_forget()
            self.id_frame_btns = {}
            self.id_frame.grid_forget()
            self.id_frame = None
        if self.zpath_frame is not None:
            for zpath in self.zpath_frame_btns:
                self.zpath_frame_btns[zpath].grid_forget()
            self.zpath_frame_btns = {}
            self.zpath_frame.grid_forget()
            self.zpath_frame = None

    def create_loc_frames(self):
        self.destroy_loc_frames()
        self.id_frame = VerticalScrolledFrame(self.cwin)
        self.id_frame_btns = {}
        self.id_frame.grid(column=1, row=0, sticky='n')
        self.zpath_frame = VerticalScrolledFrame(self.cwin)
        self.zpath_frame_btns = {}
        self.zpath_frame.grid(column=2, row=0, sticky='n')
        csv_fullpath = os.path.join(cfg.csv_folder, 'csv_appium_gui', 'appium_gui.csv')
        row = 0
        self.ids = parse_ids(csv_fullpath)
        self.id_label = Label(self.id_frame.interior, text='IDs', width=30, bg='brown')
        self.id_label.grid(column=0, row=0, stick='ew')
        row += 1
        for _id in self.ids:
            if self.elem_selected(self.ids[_id]):
                # print "_id selected: %s" % _id
                self.id_frame_btns[_id] = Button(self.id_frame.interior, text=_id, command=self.get_id_outline_fn(_id))
                self.id_frame_btns[_id].grid(row=row, column=0, sticky='w')
                row += 1
        row = 0
        self.zpaths = parse_zpaths(csv_fullpath)
        self.zpath_label = Label(self.zpath_frame.interior, text='zpaths', width=10, bg='brown')
        self.zpath_label.grid(column=0, row=0, sticky='ew')
        row += 1
        zpath_keys = self.zpaths.keys()
        for zpath in sorted(zpath_keys):
            if self.elem_selected(self.zpaths[zpath]):
                # print "zpath selected: %s" % zpath
                self.zpath_frame_btns[zpath] = Button(self.zpath_frame.interior, text=zpath,
                                                      command=self.get_zpath_outline_fn(zpath))
                self.zpath_frame_btns[zpath].grid(row=row, column=0, sticky='w')
                row += 1
        self.id_frame.update()
        self.zpath_frame.update()
        self.cwin.update()
        self.cwin.geometry(
            '%dx%d' % (self.im_width + self.id_frame.winfo_reqwidth() + self.zpath_frame.winfo_reqwidth(),
                       self.im_canvas.winfo_reqheight()))

    def mouse_btn(self, event):
        # event.type values: 4=press, 6=motion, 5=release
        # print "type = %s, type(type) = %s, x = %d, y = %d" % (event.type, type(event.type), event.x, event.y)
        if event.type == '4':
            if event.num == 1:
                self.drag_polygon_x1 = event.x
                self.drag_polygon_y1 = event.y
            elif event.num == 3:
                if self.drag_polygon is not None:
                    self.im_canvas.delete(self.drag_polygon)
                    self.drag_polygon = None
                    self.update_loc_frames()
        elif event.type == '5':
            self.update_loc_frames()
        elif event.type == '6':
            if self.drag_polygon is not None:
                self.im_canvas.delete(self.drag_polygon)
            x1 = self.drag_polygon_x1
            y1 = self.drag_polygon_y1
            x2 = event.x
            y2 = event.y
            self.drag_polygon = self.im_canvas.create_polygon(x1, y1, x1, y2, x2, y2, x2, y1, outline='blue', fill='')
            self.drag_polygon_x2 = x2
            self.drag_polygon_y2 = y2

    def get_id_outline_fn(self, id_name):
        def f():
            self.outline_elems(self.ids[id_name])
            self.find_by_var.set('id')
            self.find_value_var.set(id_name)
        return f

    def get_zpath_outline_fn(self, zpath):
        def f():
            self.outline_elems(self.zpaths[zpath])
            self.find_by_var.set('zpath')
            self.find_value_var.set(zpath)
        return f

    def on_canvas_closing(self):
        self.im_canvas = None
        self.id_frame_btns = {}
        self.id_frame = None
        self.zpath_frame_btns = {}
        self.zpath_frame = None
        self.drag_polygon = None
        self.cwin.destroy()
        # self.bottom_frame.mk_canvas.configure(state=NORMAL)

    def create_log_frame(self):
        log_frame = LogFrame(self)
        sys.stdout = log_frame
        log_frame.grid_columnconfigure(0, weight=1)
        log_frame.grid_rowconfigure(0, weight=1)
        log_frame.grid(row=self.top_frame_row, column=0, padx=2, pady=2, sticky='news')
        self.grid_rowconfigure(self.top_frame_row, weight=1)
        self.top_frame_row += 1
        return log_frame

    def create_softphone_frame(self):
        softphone_frame = Frame(self, bg='brown')
        softphone_frame.columnconfigure(0, weight=1)
        softphone_frame.grid(row=self.top_frame_row, column=0, sticky='news', padx=2)
        softphone_frame.row = self.top_frame_row
        self.top_frame_row += 1
        return softphone_frame

    def populate_softphone_frame(self):
        self.softphone_frame.account1_frame = AccountFrame(self.softphone_frame, cfg.site['DefaultSoftphoneUser'])
        self.softphone_frame.account1_frame.grid(row=0, column=0, sticky='ew', padx=2, pady=2)
        self.softphone_frame.account2_frame = AccountFrame(self.softphone_frame, cfg.site['DefaultForwardAccount'])
        self.softphone_frame.account2_frame.grid(row=1, column=0, sticky='ew', padx=2, pady=2)
        self.menu.delete(5)

    @staticmethod
    def defocus(event):
        event.widget.selection_clear()

    def create_exec_frame(self):
        exec_frame = Frame(self, bg="brown")
        exec_frame.btn = Button(exec_frame, text="exec:", command=lambda: self.do_cmd(self.exec_code), state=NORMAL)
        exec_frame.btn.grid(row=0, column=0)
        exec_frame.entry = Entry(exec_frame, textvariable = self.exec_text)
        exec_frame.entry.grid(row=0, column=1, sticky='news')
        exec_frame.columnconfigure(1, weight=1)
        exec_frame.grid(row=self.top_frame_row, column=0, padx=4, pady=4, sticky='news')
        self.top_frame_row += 1
        return exec_frame

    def exec_code(self):
        text = self.exec_text.get()
        try:
            exec text in globals()
        except Exception as e:
            print "exec raised exception: %s" % e

    def create_btn_frame(self):
        btn_frame_row = 0
        btn_frame = ButtonFrame(self, bg="brown")
        btn_frame.find_frame = Frame(btn_frame, bg='tan')
        btn = Button(btn_frame.find_frame, text="find elements:", command=lambda: self.do_cmd(self.find_elements),
                     state=DISABLED)
        self.appium_btns.append(btn)
        self.find_by_var = StringVar()
        self.find_by_var.set('uia_text')
        btn_frame.find_frame.by = Combobox(btn_frame.find_frame, width=16,
                                           values=['uia_text', 'zpath', 'xpath', 'id', '-android uiautomator',
                                                   'contacts_locator', 'voicemail_locator', 'history_locator',
                                                   'dial_locator', 'prefs_locator', 'contacts_locator_all',
                                                   'voicemail_locator_all', 'history_locator_all', 'dial_locator_all',
                                                   'prefs_locator_all'
                                                   ],
                                           textvariable=self.find_by_var, state='readonly', takefocus=False)
        btn_frame.find_frame.by.bind('<<ComboboxSelected>>', self.update_find_cbs)
        btn_frame.find_frame.by.bind("<FocusIn>", self.defocus)
        btn_frame.find_frame.by.grid(row=0, column=1, padx=2, pady=2, sticky='ew')
        self.use_parent = IntVar()
        self.use_parent.set(0)
        btn_frame.find_frame.use_parent = Checkbutton(btn_frame.find_frame, text='from Parent',
                                                      variable=self.use_parent, state=DISABLED)
        btn_frame.find_frame.use_parent.grid(row=0, column=2, padx=2, pady=2, sticky='ew')
        self.within_frame.set(0)
        btn_frame.find_frame.within_frame = Checkbutton(btn_frame.find_frame, text='within frame',
                                                        variable=self.within_frame, state=DISABLED)
        btn_frame.find_frame.within_frame.grid(row=1, column=2, padx=2, pady=2, sticky='ew')
        self.find_value_var = StringVar()
        btn_frame.find_frame.value = Combobox(btn_frame.find_frame, width=60,
                                              values=sorted(self.locators.keys(),
                                                            key=lambda x: self.locators[x]['time'], reverse=True),
                                              textvariable=self.find_value_var)
        btn_frame.find_frame.value.bind('<<ComboboxSelected>>', self.update_find_frame)
        btn_frame.find_frame.value.bind("<FocusIn>", self.defocus)
        btn_frame.find_frame.hsb = Scrollbar(btn_frame.find_frame, orient=HORIZONTAL,
                                             command=btn_frame.find_frame.value.xview)
        btn_frame.find_frame.value["xscrollcommand"] = btn_frame.find_frame.hsb.set
        btn.grid(row=0, column=0, padx=2, pady=2)
        btn_frame.find_frame.grid_columnconfigure(3, weight=1)
        btn_frame.find_frame.value.grid(row=0, column=3, padx=2, pady=2, sticky='ew')
        btn_frame.find_frame.hsb.grid(row=1, column=3, sticky='ew')
        btn_frame.find_frame.grid(row=btn_frame_row, column=0, sticky='ew', padx=2, pady=2)
        btn_frame_row += 1
        btn_frame.key_code_frame = Frame(btn_frame, bg='tan')
        btn = Button(btn_frame.key_code_frame, text="send keycode:", command=self.send_keycode, state=DISABLED)
        self.appium_btns.append(btn)
        self.keycode_name = StringVar()
        combobox = Combobox(btn_frame.key_code_frame, width=16, values=keycodes.keys(),
                            textvariable=self.keycode_name, state='readonly', takefocus=False)
        combobox.set(keycodes.keys()[-1])
        combobox.bind("<FocusIn>", self.defocus)
        btn_frame.key_code_frame.value = combobox
        btn.grid(row=0, column=0, padx=2, pady=2, sticky='w')
        btn_frame.key_code_frame.grid_columnconfigure(1, weight=1)
        btn_frame.key_code_frame.value.grid(row=0, column=1, padx=2, pady=2, sticky='w')
        y_entry = Entry(btn_frame.key_code_frame, width=4, textvariable=self.tap_y_var)
        self.appium_btns.append(y_entry)
        x_entry = Entry(btn_frame.key_code_frame, width=4, textvariable=self.tap_x_var)
        self.appium_btns.append(x_entry)
        btn = Button(btn_frame.key_code_frame, text="tap:", command=self.tap_xy, state=DISABLED)
        self.appium_btns.append(btn)
        btn.grid(row=0, column=2, padx=2, pady=2, sticky='w')
        Label(btn_frame.key_code_frame, text=" x:").grid(row=0, column=3)
        x_entry.grid(row=0, column=4, padx=2, pady=2, sticky='w')
        Label(btn_frame.key_code_frame, text=" y:").grid(row=0, column=5)
        y_entry.grid(row=0, column=6, padx=2, pady=2, sticky='w')
        y1_entry = Entry(btn_frame.key_code_frame, width=4, textvariable=self.swipe_y1_var)
        self.appium_btns.append(y1_entry)
        y2_entry = Entry(btn_frame.key_code_frame, width=4, textvariable=self.swipe_y2_var)
        self.appium_btns.append(y2_entry)
        ms_entry = Entry(btn_frame.key_code_frame, width=4, textvariable=self.swipe_ms_var)
        self.swipe_ms_var.set(100)
        self.appium_btns.append(ms_entry)
        Label(btn_frame.key_code_frame, text="   ", bg='tan').grid(row=0, column=7)
        btn = Button(btn_frame.key_code_frame, text="swipe:", command=self.swipe, state=DISABLED)
        self.appium_btns.append(btn)
        btn.grid(row=0, column=8, padx=2, pady=2, sticky='w')
        Label(btn_frame.key_code_frame, text=" y1:").grid(row=0, column=9)
        y1_entry.grid(row=0, column=10, padx=2, pady=2, sticky='w')
        Label(btn_frame.key_code_frame, text=" y2:").grid(row=0, column=11)
        y2_entry.grid(row=0, column=12, padx=2, pady=2, sticky='w')
        btn_frame.key_code_frame.grid(row=btn_frame_row, column=0, sticky='ew', padx=2, pady=2)
        Label(btn_frame.key_code_frame, text=" ms:").grid(row=0, column=13)
        ms_entry.grid(row=0, column=14, padx=2, pady=2, sticky='w')
        btn_frame.key_code_frame.grid(row=btn_frame_row, column=0, sticky='ew', padx=2, pady=2)
        btn_frame_row += 1
        self.attr_frame = AttrFrame(btn_frame, bg='tan')
        self.attr_frame.index_label = Label(self.attr_frame, text="select elem:", bg="tan")
        self.attr_frame.index_label.grid(row=0, column=0, padx=2, pady=2, sticky='e')
        self.elem_index = StringVar()
        self.elem_index.set('')
        self.attr_frame.index = Combobox(self.attr_frame, width=6, values=[], textvariable=self.elem_index)
        self.attr_frame.index.grid(row=0, column=1, padx=2, pady=2, sticky='e')
        btn = Button(self.attr_frame, text="get elem attributes", command=self.get_elem_attrs, state=DISABLED, padx=1)
        self.appium_btns.append(btn)
        btn.grid(row=0, column=2, padx=2, pady=2)
        btn = Button(self.attr_frame, text="get elem color", command=self.get_elem_color, state=DISABLED, padx=1)
        self.appium_btns.append(btn)
        btn.grid(row=0, column=3, padx=2, pady=2)
        btn = Button(self.attr_frame, text="click elem", command=self.click_element, state=DISABLED, padx=1)
        self.appium_btns.append(btn)
        btn.grid(row=0, column=4, padx=2, pady=2)
        btn = Button(self.attr_frame, text="clear elem", command=self.clear_element, state=DISABLED, padx=1)
        self.appium_btns.append(btn)
        btn.grid(row=0, column=5, padx=2, pady=2)
        btn = Button(self.attr_frame, text="set parent", command=self.set_parent, state=DISABLED, padx=1)
        self.appium_btns.append(btn)
        btn.grid(row=0, column=6, padx=2, pady=2)
        btn = Button(self.attr_frame, text="set frame", command=self.set_frame, state=DISABLED, padx=1)
        self.appium_btns.append(btn)
        btn.grid(row=0, column=7, padx=2, pady=2)
        self.attr_frame.grid(row=btn_frame_row, column=0, sticky='ew', padx=2, pady=2)
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid(row=self.top_frame_row, column=0, sticky='news', padx=2, pady=2)
        btn_frame.row = self.top_frame_row
        self.top_frame_row += 1
        return btn_frame

    def update_find_frame(self, event):
        if self.find_value_var.get() in self.locators:
            self.find_by_var.set(self.locators[self.find_value_var.get()]["by"])
            self.update_find_cbs(None)
            if self.parent_element is not None:
                self.use_parent.set(self.locators[self.find_value_var.get()]["use_parent"])
            else:
                self.use_parent.set(0)

    def create_menus(self, parent):
        menu = MyMenu(parent)
        menu.appium_sub_menu = MyMenu(menu)
        menu.appium_sub_menu_max_index = 0
        menu.add_cascade(label="Appium Actions", menu=menu.appium_sub_menu)
        menu.other_sub_menu = MyMenu(menu)
        menu.other_sub_menu_max_index = 0
        menu.add_cascade(label="Other Actions", menu=menu.other_sub_menu)
        for command in self.appium_commands:
            menu.appium_sub_menu.add_command(label=command.label, command=command.action)
            menu.appium_sub_menu_max_index += 1
        for command in self.other_commands:
            menu.other_sub_menu.add_command(label=command.label, command=command.action)
            menu.other_sub_menu_max_index += 1
        menu.add_command(label="Start Appium", command=lambda: self.do_cmd(self.open_appium))
        menu.add_command(label="Get Focused App", command=lambda: self.do_cmd(self.get_focused_app))
        menu.add_command(label="Create Softphones", command=self.populate_softphone_frame)
        parent.config(menu=menu)
        return menu

    def create_commands(self):
        self.appium_commands.append(Command("set coworker favorites", lambda: self.do_cmd(self.set_favs)))
        self.appium_commands.append(Command("clear coworker favorites", lambda: self.do_cmd(self.clear_favs)))
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
        self.appium_commands.append(Command("Restart Appium", lambda: self.do_cmd(self.restart_appium)))
        self.appium_commands.append(Command("Set Alpha OTA Server", lambda: self.do_cmd(self.set_alpha_ota_server)))
        self.appium_commands.append(Command("Skip Walkthrough", lambda: self.do_cmd(self.skip_walkthrough)))
        self.appium_commands.append(Command("Startup", lambda: self.do_cmd(self.startup)))
        self.appium_commands.append(Command("Toggle Multi-Edit", lambda: self.do_cmd(self.toggle_multi_edit)))
        self.appium_commands.append(Command("Get Digit Centers", lambda: self.do_cmd(self.get_digit_centers)))
        self.appium_commands.append(Command("VM scroll to top", lambda: self.do_cmd(self.scroll_to_top_vm)))
        self.other_commands.append(Command("Enable USB", lambda: self.do_cmd(self.usb_enable)))
        self.other_commands.append(
            Command("Get Alpha Current Versions", lambda: self.do_cmd(self.get_alpha_current_versions)))
        self.other_commands.append(
            Command("Get Beta Current Versions", lambda: self.do_cmd(self.get_beta_current_versions)))
        self.other_commands.append(Command("Get Installed Versions", lambda: self.do_cmd(self.get_installed_versions)))
        self.other_commands.append(
            Command("Get Production Current Versions", lambda: self.do_cmd(self.get_prod_current_versions)))
        self.other_commands.append(Command("Reboot", lambda: self.do_cmd(self.reboot)))
        self.other_commands.append(Command("Remove APK Upgrades", lambda: self.do_cmd(remove_apk_upgrades)))
        self.other_commands.append(
            Command("Force AOSP Downgrade to 2.3.12", lambda: self.do_cmd(self.force_aosp_downgrade)))

    def do_cmd(self, cmd):
        for btn in self.appium_btns:
            btn.configure(state=DISABLED)
        for btn in self.no_appium_btns:
            btn.configure(state=DISABLED)
        for i in range(self.menu.appium_sub_menu_max_index):
            self.menu.appium_sub_menu.entryconfig(i + 1, state=DISABLED)
        for i in range(self.menu.other_sub_menu_max_index):
            self.menu.other_sub_menu.entryconfig(i + 1, state=DISABLED)
        for i in [3, 4]:
            self.menu.entryconfig(i, state=DISABLED)
        self.update_idletasks()
        # sleep(5)
        self.worker_thread = threading.Thread(target=cmd, name=cmd)
        self.worker_thread.start()
        log.debug("worker thread started")
        self.after(100, self.check_thread)

    def close_appium_and_quit(self):
        if self.appium_is_open:
            self.close_appium()
        try:
            os.mkdir('tmp')
        except OSError:
            pass
        with open('tmp/appium_gui_locators.json', 'w') as f:
            f.write(json.dumps(self.locators, sort_keys=True, indent=4, separators=(',', ': ')))
        root.destroy()

    def send_keycode(self):
        keycode_name = self.keycode_name.get()
        keycode = keycodes[keycode_name]
        print "sending keycode %s (value %d)" % (keycode_name, keycode)
        # base_view.driver.keyevent(keycode)
        base_view.send_keycode(keycode_name)

    def tap_xy(self):
        try:
            x = int(self.tap_x_var.get())
            y = int(self.tap_y_var.get())
        except (ValueError, TypeError) as e:
            print "Can't execute tap with x='%s', y='%s'" % (self.tap_x_var.get(), self.tap_y_var.get())
        else:
            print "Executing tap([(%d, %d)])..." % (x, y),
            base_view.tap([(x, y)])
            print "Done"

    def swipe(self):
        try:
            y1 = int(self.swipe_y1_var.get())
            y2 = int(self.swipe_y2_var.get())
            ms = int(self.swipe_ms_var.get())
        except (ValueError, TypeError) as e:
            print "Can't execute swipe with x='%s', y='%s'" % (self.tap_x_var.get(), self.tap_y_var.get())
        else:
            print "Executing swipe([(300, %d, 300, %d, %d)])..." % (y1, y2, ms),
            base_view.long_press_swipe(300, y1, 300, y2, duration=ms)
            print "Done"

    def update_find_cbs(self, event):
        find_by = self.find_by_var.get()
        if (find_by == 'id') and self.parent_element is not None:
            self.btn_frame.find_frame.use_parent.configure(state=NORMAL)
        else:
            self.btn_frame.find_frame.use_parent.configure(state=DISABLED)
            self.use_parent.set(0)
        if find_by[-11:] == 'locator_all' and self.frame_element is not None:
            self.btn_frame.find_frame.within_frame.configure(state=NORMAL)
        else:
            self.btn_frame.find_frame.within_frame.configure(state=DISABLED)

    def find_elements_by_locator_name(self, by, value):
        elems = []
        try:
            if by[-3:] == 'all':
                elems = getattr(self.views[by[:-12]].all, value)
            else:
                elems = [getattr(self.views[by[:-8]], value)]
        except Ux as e:
            print e.message
        if self.within_frame.get():
            return filter(get_filter('within_frame', frame=self.frame_element), elems)
        else:
            if elems == [None]:
                return []
            return elems

    def find_elements_with_driver(self, by, value):
        if by == 'zpath':
            value = expand_zpath(value)
            by = 'xpath'
            print "xpath = %s" % value
        elif by == 'uia_text':
            by = '-android uiautomator'
            value = 'new UiSelector().text("%s")' % value
        if self.use_parent.get():
            return self.parent_element.find_elements(by, value)
        else:
            return base_view.driver.find_elements(by, value)

    def find_elements(self):
        print "finding elements...",
        by = self.find_by_var.get()
        value = self.find_value_var.get()
        use_parent = self.use_parent.get()
        if value in self.locators.keys():
            self.locators[value]['time'] = time()
        else:
            self.locators[value] = {"by": by, "use_parent": use_parent, "time": time()}
        sorted_keys = sorted(self.locators.keys(), key=lambda x: self.locators[x]['time'], reverse=True)
        for key in sorted_keys[50:]:
            del self.locators[key]
            sorted_keys.pop()
        self.btn_frame.find_frame.value.configure(value=sorted_keys)
        if by[-7:] == 'locator' or by[-11:] == 'locator_all':
            self.elems = self.find_elements_by_locator_name(by, value)
        else:
            try:
                self.elems = self.find_elements_with_driver(by, value)
            except InvalidSelectorException as e:
                print str(e).strip()
                return
            # keep frame element setting if using "by" value ending in '*_locator'
            self.frame_element = None
            self.within_frame.set(0)
        print "%s element%s found" % (len(self.elems), '' if len(self.elems) == 1 else 's')
        elem_indices = [str(i) for i in range(len(self.elems))]
        self.attr_frame.index.configure(values=elem_indices)
        if len(elem_indices):
            self.elem_index.set('0')
        else:
            self.elem_index.set('')
        self.parent_element = None
        self.btn_frame.find_frame.use_parent.configure(state=DISABLED)
        self.use_parent.set(0)
        self.update_find_cbs(None)

    def get_elem_attrs(self):
        text_index = self.elem_index.get()
        if text_index == '':
            return
        index = int(text_index)
        elem = self.elems[index]
        print "\nattributes for element %d" % index
        print "  %10s: %s" % ("location_in_view", elem.location_in_view)
        print "  %10s: %s" % ("location", elem.location)
        print "  %10s: %s" % ("size", elem.size)
        for attr in ['name', 'contentDescription', 'text', 'className', 'resourceId', 'enabled', 'checkable', 'checked',
                     'clickable', 'focusable', 'focused', 'longClickable', 'scrollable', 'selected', 'displayed']:
            print "  %10s:" % attr,
            try:
                print elem.get_attribute(attr)
            except NoSuchElementException:
                log.debug("NoSuchElementException running elem.get_attribute(%s)" % attr)
                print
        self.outline_elems([{
            "x1": int(elem.location['x']),
            "y1": int(elem.location['y']),
            "x2": int(elem.location['x']) + int(elem.size['width']),
            "y2": int(elem.location['y']) + int(elem.size['height'])
        }])
        pass

    def outline_elems(self, geoms):
        if hasattr(self, 'im_canvas') and self.im_canvas is not None:
            while len(self.polygons):
                self.im_canvas.delete(self.polygons.pop())
            for geom in geoms:
                x1 = int(geom["x1"] * self.cwin.scale)
                y1 = int(geom["y1"] * self.cwin.scale)
                y2 = int(geom["y2"] * self.cwin.scale)
                x2 = int(geom["x2"] * self.cwin.scale)
                # print "calling create_polygon(%d, %d, %d, %d, %d, %d, %d, %d)" % (x1, y1, x1, y2, x2, y2, x2, y1)
                self.polygons.append(self.im_canvas.create_polygon(x1, y1, x1, y2, x2, y2, x2, y1, outline='red',
                                                                   fill=''))
                pass

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
        color = base_view.get_element_color_and_count('appium_gui', elem, color_list_index=2)
        print "third color and count: %s" % color
        for color_name in ['favorite_on_color', 'favorite_off_color']:
            if base_view.color_match(color, cfg.colors['ContactsView'][color_name]):
                print color_name

    def click_element(self):
        text_index = self.elem_index.get()
        if text_index == '':
            return
        index = int(text_index)
        self.elems[index].click()

    def clear_element(self):
        text_index = self.elem_index.get()
        if text_index == '':
            return
        index = int(text_index)
        self.elems[index].clear()

    def set_parent(self):
        text_index = self.elem_index.get()
        if text_index == '':
            return
        index = int(text_index)
        self.parent_element = self.elems[index]
        self.update_find_cbs(None)

    def set_frame(self):
        text_index = self.elem_index.get()
        if text_index == '':
            return
        index = int(text_index)
        self.frame_element = self.elems[index]
        self.update_find_cbs(None)

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
        self.update_find_cbs(None)
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
        log.debug('cmd: %s\nelapsed: [%5.3f s]  \necho: "%s"\n' %
                  (action['cmd'], elapsed, repr(lines[0].encode('string_escape'))))
        for line in lines[1:]:
            log.debug(' '*7 + line.encode('string_escape'))

    def restart_appium(self):
        print "Restarting Appium...",
        self.close_appium()
        self.open_appium()
        print "Done"

    @staticmethod
    def get_focused_app():
        print "Getting Focused App...",
        app = get_focused_app()
        print "Done"
        print "Focused App: " + app

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
    def clear_favs():
        print "clearing all favorite coworkers...",
        contacts_view.clear_all_favorites()
        print "Done"

    @staticmethod
    def set_favs():
        print "setting all favorite coworkers...",
        contacts_view.set_all_favorites()
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
        ss = SpudSerial(cfg.site['SerialDev'])
        self.log_action(ss, {'cmd': 'cd\n', 'new_cwd': 'data'})
        self.log_action(ss, {'cmd': 'reboot\n', 'new_cwd': '', 'expect': 'mtp_open', 'dead_air_timeout': 20,
                             'timeout': 120})
        print "Done"

    @staticmethod
    def get_installed_versions():
        print "getting installed versions"
        # self.update_idletasks()
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
        user_view.goto_tab('Dial')
        dial_view.dial_advanced_settings()
        dial_view.touch_call_button()
        print "Done"

    @staticmethod
    def dial_alpha_ota():
        print "dialing alpha OTA code...",
        # user_view.goto_tab('Dial')
        aosp, app = get_installed_versions()
        user_view.touch_element_with_text('Dial')
        dial_view.dial_set_alpha_ota_server(aosp)
        dial_view.touch_call_button()
        print "Done"

    @staticmethod
    def dial_beta_ota():
        print "dialing beta OTA code...",
        user_view.goto_tab('Dial')
        dial_view.dial_set_beta_ota_server()
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
    def get_digit_centers():
        print "Getting digit centers...",
        user_view.goto_tab('Dial')
        for btn in ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'Star', '0', 'Pound']:
            el = dial_view.find_named_element("NumKey" + btn)
            x = int(el.location['x']) + (int(el.size['width']) / 2)
            y = int(el.location['y']) + (int(el.size['height']) / 2)
            print "%s: (%d, %d)" % (btn, x, y)
        print "Done"

    @staticmethod
    def scroll_to_top_vm():
        print "Scrolling to top of voicemail window...",
        voicemail_view.get_top_vm_parents()
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
    def get_xml():
        print "Getting XML and CSV...",
        xml = base_view.get_source()
        xml_dir = os.path.join(cfg.xml_folder, 'xml_appium_gui')
        csv_dir = os.path.join(cfg.csv_folder, 'csv_appium_gui')
        try:
            os.makedirs(xml_dir)
        except OSError as e:
            # ignore 'File exists' error but re-raise any others
            if e.errno != 17:
                raise e
        try:
            os.makedirs(csv_dir)
        except OSError as e:
            # ignore 'File exists' error but re-raise any others
            if e.errno != 17:
                raise e
        xml_fullpath = os.path.join(xml_dir, 'appium_gui.e7_xml')
        csv_fullpath = os.path.join(csv_dir, 'appium_gui.csv')
        log.info("saving e7_xml %s" % xml_fullpath)
        with open(xml_fullpath, 'w') as _f:
            _f.write(xml.encode('utf8'))
        xml_to_csv(xml_fullpath, csv_fullpath)

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
        print "Done"


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
