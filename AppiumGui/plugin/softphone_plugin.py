from Tkconstants import DISABLED, NORMAL
from Tkinter import Frame, IntVar, StringVar, Label, Checkbutton, Button
from lib.user_exception import UserException as Ux


def create_softphone_frame(self, acct_specs):
    frame = Frame(self.parent, bg='brown')
    frame.columnconfigure(0, weight=1)
    for row, acct_spec in enumerate(acct_specs):
        frame.account1_frame = AccountFrame(frame, acct_spec['label'], acct_spec['softphone'])
        frame.account1_frame.grid(row=row, column=0, sticky='ew', padx=2, pady=2)
    self.parent.top_frames.insert(1, frame)
    self.parent.populate_top_frames()
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