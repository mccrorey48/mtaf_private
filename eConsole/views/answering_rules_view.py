import mtaf.mtaf_logging as logging
from eConsole.views.logged_in_view import LoggedInView

log = logging.get_logger('mtaf.ans_rules')


class AnsweringRulesView(LoggedInView):
    select_text = '5\n10\n15\n20\n25\n30\n35\n40\n45\n50\n55\n60\n65\n70\n75\n80\n85\n90\n120\n180\n240\n300\n600\n' \
                  + '900\n1200\nUnlimited'
    form_text = 'Ring for\n' + select_text + '\nseconds'
    locators = {
        "AnsweringRulesTimeout": {"by": "id", "value": "answeringRulesTimeout"},
        "TimeFramesButton":  {"by": "css selector", "value": "button", "text": "Time Frames"},
        "AddRuleButton":  {"by": "css selector", "value": "button", "text": "Add Rule"},
        "OrderHeader": {"by": "css selector", "value": "th", "text": "Order"},
        "TimeFrameHeader": {"by": "css selector", "value": "th", "text": "Time Frame"},
        "DescriptionHeader": {"by": "css selector", "value": "th", "text": "Description"},
        "ActionsHeader": {"by": "css selector", "value": "th", "text": "Actions"},
        "RingForSelect": {"by": "css selector", "value": "select", "text": select_text},
        "RingForForm": {"by": "css selector", "value": "form", "text": form_text},
    }

    def __init__(self):
        super(AnsweringRulesView, self).__init__()
        self.banner_texts = ['Settings', 'Answering Rules']
        self.content_scopes.update({
            "OrderHeader": self.all_scopes,
            "TimeFrameHeader": self.all_scopes,
            "DescriptionHeader": self.all_scopes,
            "ActionsHeader": self.all_scopes,
            "RingForSelect": self.all_scopes,
            "RingForForm": self.all_scopes,
        })
        self.nav_tab_names = ["HOME", "MESSAGES", "CONTACTS", "PHONES", "CALL HISTORY", "SETTINGS"]
        self.view_name = 'answering_rules_view'


answering_rules_view = AnsweringRulesView()
