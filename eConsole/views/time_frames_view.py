import mtaf.mtaf_logging as logging
from eConsole.views.logged_in_view import LoggedInView

log = logging.get_logger('mtaf.time_frames')


class TimeFramesView(LoggedInView):

    locators = {
        "Banner": {"by": "css selector", "value": "span[class='esi-header-text']",
                   "text": "Settings / Time Frames"},
    }

    def __init__(self):
        super(TimeFramesView, self).__init__()
        self.presence_element_names = ["Banner"]
        self.nav_tab_names = ["HOME", "MESSAGES", "CONTACTS", "PHONES", "CALL HISTORY", "SETTINGS"]
        self.view_name = 'time_frames_view'


time_frames_view = TimeFramesView()
