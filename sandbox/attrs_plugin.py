# from attrs import MyClass
__all__ = ['change_methods']
from Tkinter import Button


def my_printme(self):
    print "class text is %s" % self.text
    print "class is %s" % self.__class__


def install(self):
    print "installing plugin for %s" % type(self)
    Button(self, text="MyPrintme", command=lambda:my_printme(self)).pack()
