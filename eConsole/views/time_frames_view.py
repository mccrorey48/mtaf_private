import mtaf.mtaf_logging as logging
from eConsole.views.logged_in_view import LoggedInView

log = logging.get_logger('mtaf.time_frames')


class TimeFramesView(LoggedInView):

    locators = {
        "ActionsHeader": {"by": "css selector", "value": "th", "text": "Actions"},
        "AddTimeFrameButton": {"by": "css selector", "value": "button[ng-click='addTimeframe()']"},
        "AnsweringRulesButton": {"by": "css selector", "value": "a[href='/#!/settings/answerRules']"},
        "AnsweringRulesButton": {"by": "css selector", "value": "a[href='/#!/settings/answerRules']"},
        "DescriptionHeader": {"by": "css selector", "value": "th", "text": "Description"},
        "NameHeader": {"by": "css selector", "value": "th", "text": "Name"},
        "OwnerHeader": {"by": "css selector", "value": "th", "text": "Owner"},
    }

    def __init__(self):
        super(TimeFramesView, self).__init__()
        self.content_scopes.update({
            "ActionsHeader": self.all_scopes,
            "AddTimeFrameButton": self.all_scopes,
            "AnsweringRulesButton": self.all_scopes,
            "DescriptionHeader": self.all_scopes,
            "NameHeader": self.all_scopes,
            "OwnerHeader": self.all_scopes,
        })
        self.nav_tab_names = ["HOME", "MESSAGES", "CONTACTS", "PHONES", "CALL HISTORY", "SETTINGS"]
        self.view_name = 'time_frames_view'


time_frames_view = TimeFramesView()
