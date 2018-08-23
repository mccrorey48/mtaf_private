from Tkinter import *

use_grid = True


class ScrollFramePack(Frame):
    def __init__(self, parent, hsb=True, vsb=True):
        Frame.__init__(self, parent)
        self.canvas = Canvas(parent, borderwidth=0, background="#88ffff")
        self.frame = Frame(self.canvas, background="#ffffff")
        if hsb:
            self.hsb = Scrollbar(parent, orient="horizontal", command=self.canvas.xview)
            self.canvas.configure(xscrollcommand=self.hsb.set)
        if vsb:
            self.vsb = Scrollbar(parent, orient="vertical", command=self.canvas.yview)
            self.canvas.configure(yscrollcommand=self.vsb.set)

        if hsb:
            self.hsb.pack(side="bottom", fill="x")
        if vsb:
            self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw",
                                  tags="self.frame")
        self.frame.bind("<Configure>", self.onFrameConfigure)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


class ScrollFrameGrid(Frame):
    def __init__(self, parent, hsb=True, vsb=True):

        Frame.__init__(self)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.canvas = Canvas(self, borderwidth=0, background="#88ffff")
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


def populate(self):
    '''Put in some fake data'''
    for row in range(10):
        Label(self.frame, text="%s" % row, width=3, borderwidth="1",
              relief="solid").grid(row=row, column=0)
        t="this is the second column for row %s" %row
        Label(self.frame, text=t).grid(row=row, column=1)


if __name__ == "__main__":
    root=Tk()
    if use_grid:
        sf = ScrollFrameGrid(root)
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        sf.grid(row=0, column=0, sticky='nsew')
    else:
        sf = ScrollFramePack(root)
        sf.pack(side="top", fill="both", expand=True)
    populate(sf)
    root.mainloop()