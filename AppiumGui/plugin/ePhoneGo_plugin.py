from ePhone7_plugin.views import *
from ePhone7_plugin.utils.usb_enable import usb_enable
from ePhone7_plugin.utils.versions import get_installed_versions


class EGoCommands(object):
    pass



ego_cmds = EGoCommands()

cmd_types = {
    # 'Appium Actions': [
    #     {'label': 'Dial Advanced Settings Code', 'command': e7_cmds.dial_advanced_settings},
    #     {'label': 'Dial Alpha OTA Code', 'command': e7_cmds.dial_alpha_ota},
    #     {'label': 'Dial Beta OTA Code', 'command': e7_cmds.dial_beta_ota},
    #     {'label': 'Dial Current OTA Code', 'command': e7_cmds.dial_show_ota},
    #     {'label': 'Dial Production OTA Code', 'command': e7_cmds.dial_prod_ota},
    #     {'label': 'Set Coworker Favorites', 'command': e7_cmds.set_favorites}
    # ],
    # 'Other Actions': [
    #     {'label': 'Enable USB', 'command': e7_cmds.usb_enable}
    # ]
}


# appium_gui.py instantiates the AppiumGui class, then calls install(), passing the AppiumGui instance as an argument
def install(self):

    # - install drop-down menu items appropriate for ePhone7
    # - "cmd_types" key values are the labels for drop-down menus in AppiumGui
    # - new commands listed in "cmd_types[key]" are added to the menu labeled with that key
    # - if there is no drop-down menu labeled with a key, a new drop-down menu will be created
    for cmd_type in cmd_types:
        if cmd_type not in self.menu.submenus:
            self.menu.add_submenu(cmd_type)
        for cmd_spec in cmd_types[cmd_type]:
            self.menu.submenus[cmd_type].add_command(label=cmd_spec['label'], command=cmd_spec['command'])

    # add locator type options for variouis ePhone7 views
    values = self.btn_frame.find_frame.by.cget('values')
    values += ('contacts_locator', 'voicemail_locator', 'history_locator',
               'dial_locator', 'prefs_locator', 'contacts_locator_all',
               'voicemail_locator_all', 'history_locator_all', 'dial_locator_all',
               'prefs_locator_all')
    self.btn_frame.find_frame.by.configure(values=values)


