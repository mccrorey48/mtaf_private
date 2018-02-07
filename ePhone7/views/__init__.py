from .active_call_view import active_call_view
from .advanced_settings_view import advanced_settings_view
from .app_intro_view import app_intro_view
from .base_view import base_view
from .contacts_view import contacts_view
from .contact_detail_view import contact_detail_view
from .dial_view import dial_view
from .history_view import history_view
from .home_view import home_view
from .login_view import login_view
from .network_view import network_view
from .prefs_view import prefs_view
from .tnc_view import tnc_view
from .user_view import user_view
from .voicemail_view import voicemail_view

view_dict = {
    'active_call': active_call_view,
    'active call': active_call_view,
    'advanced_settings': advanced_settings_view,
    'advanced settings': advanced_settings_view,
    'app_intro': app_intro_view,
    'app intro': app_intro_view,
    'base': base_view,
    'contacts': contacts_view,
    'dial': dial_view,
    'history': history_view,
    'home': home_view,
    'login': login_view,
    'network': network_view,
    'prefs': prefs_view,
    'preferences': prefs_view,
    'tnc': tnc_view,
    'user': user_view,
    'voicemail': voicemail_view
}


class AllViews(object):
    def __getitem__(self, view_name):
        return self.__getattr__(view_name)

    def __getattr__(self, view_name):
        view_name = view_name.lower()
        if view_name[-4:] == 'view':
            view_name = view_name[:-4]
        elif view_name[-5:] == '_view':
            view_name = view_name[:-5]
        if view_name in view_dict:
            return view_dict[view_name]
        else:
            return None


all_views = AllViews()
