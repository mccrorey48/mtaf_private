from .auto_attendants_view import auto_attendants_view
from .base_view import base_view
from .call_history_view import call_history_view
from .contacts_view import contacts_view
from .home_view import home_view
from .login_view import login_view
from .manage_home_view import manage_home_view
from .message_settings_view import message_settings_view
from .messages_view import messages_view
from .phones_view import phones_view

view_dict = {
    'auto_attendants_view': auto_attendants_view,
    'base_view': base_view,
    'call_history_view': call_history_view,
    'contacts_view': contacts_view,
    'home_view': home_view,
    'login_view': login_view,
    'manage_home_view': manage_home_view,
    'message_settings_view': message_settings_view,
    'messages_view': messages_view,
    'phones_view': phones_view
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
