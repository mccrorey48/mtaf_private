from ePhone7.views.contacts_view import contacts_view
from ePhone7.views.history_view import history_view
from ePhone7.views.voicemail_view import voicemail_view
# from ePhone7.views.keypad import keypad_view
from ePhone7.views.user_view import user_view
view_info = {
    'user': {
        'view_instance': user_view,
        'view_classname': 'UserView',
        'tabs': {
            'contacts': {
                'locator_name': 'Contacts'
            },
            'history': {
                'locator_name': 'History'
            },
            'voicemail': {
                'locator_name': 'Voicemail'
            },
            'dial_number': {
                'locator_name': 'Keypad'
            }
        }
    },
    'contacts': {
        'view_tab': 'Contacts',
        'view_classname': 'ContactsView',
        'view_instance': contacts_view,
        'tabs': {
            'personal': {
                'locator_name': 'Personal'
            },
            'coworkers': {
                'locator_name': 'Coworkers'
            },
            'favorites': {
                'locator_name': 'Favorites'
            },
            'groups': {
                'locator_name': 'Groups'
            }
        }
    },
    'history': {
        'view_tab': 'History',
        'view_classname': 'HistoryView',
        'view_instance': history_view,
        'tabs': {
            'all': {
                'locator_name': 'All'
            },
            'missed': {
                'locator_name': 'Missed'
            }
        }
    },
    'voicemail': {
        'view_tab': 'Voicemail',
        'view_classname': 'VoicemailView',
        'view_instance': voicemail_view,
        'tabs': {
            'new': {
                'locator_name': 'New'
            },
            'saved': {
                'locator_name': 'Saved'
            },
            'trash': {
                'locator_name': 'Trash'
            }
        }
    }
}

