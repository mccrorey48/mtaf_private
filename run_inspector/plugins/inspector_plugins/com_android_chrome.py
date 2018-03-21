class Plugin(object):

    def install_plugin(self, _app):

        def hello():
            print "Hello, World"

        def goodbye():
            print "Goodbye, World"

        cmd_types = {
            'ADB Actions': [
                {'label': 'Print Hello World', 'command': hello},
            ],
            'Other Actions': [
                {'label': 'Print Goodbye World', 'command': goodbye},
            ]
        }
        for cmd_type in cmd_types:
            if cmd_type not in _app.menu.submenus:
                _app.menu.add_submenu(cmd_type)
            for cmd_spec in cmd_types[cmd_type]:
                _app.menu.submenus[cmd_type].add_command(label=cmd_spec['label'], command=cmd_spec['command'])

        _app.set_zpath_tag('ws', 'com.android.launcher3.Workspace')
