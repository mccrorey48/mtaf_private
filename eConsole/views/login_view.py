import lib.logging_esi as logging

from eConsole.config.configure import cfg
from eConsole.views.base_view import BaseView
from lib.wrappers import Trace

log = logging.get_logger('esi.login_view')


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

    @Trace(log)
    def input_username(self, scope):
        username = [account['email'] for account in cfg.site['accounts'] if account['scope'] == scope][0]
        log.debug("username = %s" % username)
        self.input_text(username, 'UserName')

    @Trace(log)
    def input_password(self, scope):
        password = [account['password'] for account in cfg.site['accounts'] if account['scope'] == scope][0]
        log.debug("password = %s" % password)
        self.input_text(password, 'Password')

    @Trace(log)
    def click_login_button(self):
        self.click_named_element('LoginButton')


login_view = LoginView()
