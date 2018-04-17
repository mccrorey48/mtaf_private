import six
if six.PY3:
    from tkinter import *
    from tkinter import simpledialog as tk_simple_dialog
    from tkinter.ttk import Combobox
else:
    from Tkinter import *

class MenuApp(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg='brown')
        self.menubar = Menu(self)
        self.items = Menu(self.menubar)
        self.menubar.add_cascade(label='Cascade', menu=self.items)
        self.items.add_command(label='Hello, world', command=self.hello)
        self.items.add_command(label='Goodbye, world', command=self.quit)
        self.items.entryconfig(1, state=DISABLED)
        parent.config(menu=self.menubar)
        Label(self, text="Menu Example", anchor=W, width=30).grid(row=0, column=0)
        Button(self, text="Quit", command=quit).grid(row=1, column=0, sticky='e')
        self.grid(row=0, column=0)

    def hello(self):
        print "Hello!"



root = Tk()
root.wm_title("Menu example")
# w = Label(root, text="Hello")
w = MenuApp(root)
# w.grid(row=0, column=0)
w.mainloop()
