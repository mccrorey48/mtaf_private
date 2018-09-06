class DriverActions(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, f):
        def wrapped(*args, **kwargs):
            if Actions.get_instance().driver is None:
                print "no %s!" % self.name
            else:
                print "%s is %s" % (self.name, Actions.get_instance().driver)
                f(*args, **kwargs)

        return wrapped


class Actions(object):
    driver = None
    __instance = None

    def __init__(self):
        if Actions.__instance is None:
            Actions.__instance = self

    @staticmethod
    def get_instance():
        if Actions.__instance is None:
            Actions()
        return Actions.__instance

    @DriverActions('browser')
    def action(self):
        print "action: self.driver = %s" % self.driver


class DerivedActions(Actions):
    def __init__(self):
        super(DerivedActions, self).__init__()


a = Actions.get_instance()
# a = Actions()
# print a
b = Actions.get_instance()
# b = Actions()
# print b
a.action()
Actions.driver = 'firefox'
a.action()
d = DerivedActions()
d.action()