import lib.mtaf_logging as logging

from WebApp.views.base import BaseView
from lib.trace import Trace

log = logging.get_logger('mtaf.start_view')


class StartView(BaseView):

    locators = {
        "SignInButton": {"by": "link text", "value": "Sign in"}
    }

    def __init__(self):
        super(StartView, self).__init__()
        self.view_name = "start"
        self.page_title = "My Store"

    @Trace(log)
    def goto_login(self):
        self.find_named_element('SignInButton').click()


start_view = StartView()
