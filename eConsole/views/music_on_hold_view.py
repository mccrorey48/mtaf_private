import mtaf.mtaf_logging as logging
from eConsole.views.logged_in_view import LoggedInView

log = logging.get_logger('mtaf.moh')


class MusicOnHoldView(LoggedInView):

    locators = {
        "ActionsHeader": {"by": "css selector", "value": "th", "text": "Actions"},
        "ActiveHeader": {"by": "css selector", "value": "th", "text": "Active"},
        "AddMusicButton": {"by": "css selector", "value": "button[ng-click='preAddMusicSetting()']", "text": "Add Music"},
        "DurationHeader": {"by": "css selector", "value": "th", "text": "Duration"},
        "FileSizeHeader": {"by": "css selector", "value": "th", "text": "File Size"},
        "SettingsButton": {"by": "css selector", "value": "button[ng-click='preSettingMusic()']", "text": "Settings"},
        "SongNameHeader": {"by": "css selector", "value": "th", "text": "Song Name"},
    }

    def __init__(self):
        super(MusicOnHoldView, self).__init__()
        self.banner_texts = ['Settings', 'Music on Hold']
        self.content_scopes.update({
         "ActionsHeader": self.all_scopes,
         "ActiveHeader": self.all_scopes,
         "AddMusicButton": self.all_scopes,
         "DurationHeader": self.all_scopes,
         "FileSizeHeader": self.all_scopes,
         "SettingsButton": self.all_scopes,
         "SongNameHeader": self.all_scopes,
        })
        self.nav_tab_names = ["HOME", "MESSAGES", "CONTACTS", "PHONES", "CALL HISTORY", "SETTINGS"]
        self.view_name = 'music_on_hold_view'


music_on_hold_view = MusicOnHoldView()
