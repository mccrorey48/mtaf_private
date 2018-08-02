import mtaf.mtaf_logging as logging

from eConsole.views.base_view import BaseView
from mtaf.trace import Trace

log = logging.get_logger('mtaf.login')


class LoginView(BaseView):

    locators = {
        "LoginButton": {"by": "id", "value": "loginButton"},
        "Password": {"by": "id", "value": "password"},
        "UserName": {"by": "id", "value": "username"}
    }

    def __init__(self):
        super(LoginView, self).__init__()
        self.page_title = "ESI"
        self.presence_element_names = ["LoginButton", "Password", "UserName"]
        self.view_name = 'login'

    @Trace(log)
    def input_username(self, username):
        self.input_text(username, 'UserName')

    @Trace(log)
    def input_password(self, password):
        self.input_text(password, 'Password')

    @Trace(log)
    def click_login_button(self):
        self.click_named_element('LoginButton')


login_view = LoginView()
