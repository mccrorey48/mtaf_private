import lib.mtaf_logging as logging

from WebApp.views.base import BaseView
from lib.trace import Trace

log = logging.get_logger('mtaf.user_home_view')


class UserHomeView(BaseView):

    locators = {
    }

    def __init__(self):
        super(UserHomeView, self).__init__()
        self.view_name = "home"
        self.page_title = "My account - My Store"

    @Trace(log)
    def goto_login(self):
        self.find_named_element('SignInButton').click()


user_home_view = UserHomeView()
