from Tkinter import Frame, Button, Tk


class MyClass(Frame):
    text = 'foobar'

    def __init__(self, parent):
        Frame.__init__(self, parent)
        Button(self, text='Quit', command=self.quit).pack()
        Button(self, text='Printme', command=self.printme).pack()
        self.pack()

    def install_plugin(self, plugin):
        plugin.install(self)

    def printme(self):
        print "MyClass printme()"

    def __nonzero__(self):
        return True



root = Tk()
import attrs_plugin
mc = MyClass(root)
mc.install_plugin(attrs_plugin)
mc.mainloop()
