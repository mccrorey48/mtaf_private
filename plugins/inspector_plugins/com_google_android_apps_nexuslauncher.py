import six


class NexusCommands:

    def __init__(self, app):
        self.app = app

    @staticmethod
    def print_hello():
        six.print_("Hello, World")

    @staticmethod
    def print_goodbye():
        six.print_("Goodbye, World")


class Plugin(object):

    @staticmethod
    def install_plugin(app):

        nexus_cmds = NexusCommands(app)
        app.user_cmds.update({
            'Print Hello World': nexus_cmds.print_hello,
            'Print Goodbye World': nexus_cmds.print_goodbye,
        })
        menu_items = {
            'ADB Actions': [
                {'label': 'Print Hello World', 'uses_appium': False},
            ],
            'Other Actions': [
                {'label': 'Print Goodbye World', 'uses_appium': False},
            ]
        }
        for menu_label in menu_items:
            app.menu.add_submenu(menu_label, app.make_menu_items(menu_items[menu_label]))
        app.menu.enable_items(app.appium_is_open)
        app.set_zpath_tag('ws', 'com.android.launcher3.Workspace')
