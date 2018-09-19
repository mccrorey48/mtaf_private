import six


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
    #   btn = Button(...)print ai.foo
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
        # six.print_("AutoIncrementer returning %s for name %s" % (last_count, name))
        return self.last_count


ai = AutoIncrementer()
six.print_(ai.foo)
six.print_(ai.foo)
six.print_(ai.foo)
six.print_(ai.last_count)
six.print_(ai.foo)
six.print_(ai.last_count)

