from softphone_plugin import create_softphone_frame
from ePhoneGoAndroid.config.configure import cfg
from ePhoneGoAndroid.utils.get_softphone import get_softphone
from lib.android_zpath import set_zpath_tag


class EGoCommands(object):

    def __init__(self, parent):
        self.parent = parent

    def create_softphone_frames(self):
        acct_specs = []
        for username in [cfg.site['DefaultSoftphoneUser'], cfg.site['DefaultForwardAccount']]:
            softphone = get_softphone(username)
            softphone.set_incoming_response(180)
            acct_specs.append({'label': username, 'softphone': softphone})
        self.parent.softphone_frame = create_softphone_frame(self, acct_specs)


# appium_gui.py instantiates the AppiumGui class, then calls install(), passing the AppiumGui instance as an argument
def install(parent):

    # - install drop-down menu items appropriate for ePhone7
    # - "cmd_types" key values are the labels for drop-down menus in AppiumGui
    # - new commands listed in "cmd_types[key]" are added to the menu labeled with that key
    # - if there is no drop-down menu labeled with a key, a new drop-down menu will be created

    ego_cmds = EGoCommands(parent)
    cmd_types = {
        # 'Appium Actions': [
        #     {'label': 'Dial Advanced Settings Code', 'command': ego_cmds.dial_advanced_settings},
        #     {'label': 'Set Coworker Favorites', 'command': ego_cmds.set_favorites}
        # ]
        'Other Actions': [
            {'label': 'Create Softphones', 'command': ego_cmds.create_softphone_frames},
        ]
    }
    for cmd_type in cmd_types:
        if cmd_type not in parent.menu.submenus:
            parent.menu.add_submenu(cmd_type)
        for cmd_spec in cmd_types[cmd_type]:
            parent.menu.submenus[cmd_type].add_command(label=cmd_spec['label'], command=cmd_spec['command'])

    # add locator type options for variouis ePhoneGo views
    # values = parent.btn_frame.find_frame.by.cget('values')
    # values += ('contacts_locator', 'voicemail_locator', 'history_locator',
    #            'dial_locator', 'prefs_locator', 'contacts_locator_all',
    #            'voicemail_locator_all', 'history_locator_all', 'dial_locator_all',
    #            'prefs_locator_all')
    # parent.btn_frame.find_frame.by.configure(values=values)
    set_zpath_tag('llc', 'android.support.v7.widget.LinearLayoutCompat')


