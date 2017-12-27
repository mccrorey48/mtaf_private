import lib.mtaf_logging as logging

from WebApp.config.configure import cfg
from WebApp.views.base import BaseView
from lib.trace import Trace

log = logging.get_logger('mtaf.login_view')


class LoginView(BaseView):

    locators = {
        "InvalidLoginAlert": {"by": "class name", "value": "alert-danger",
                              "partial text": "There is 1 error"},
        "LoginButton": {"by": "id", "value": "SubmitLogin"},
        "Password": {"by": "id", "value": "passwd"},
        "UserName": {"by": "id", "value": "email"}
    }

    def __init__(self):
        super(LoginView, self).__init__()
        self.view_name = "login"
        self.page_title = "Login - My Store"

    @Trace(log)
    def input_bad_password(self):
        el = self.find_named_element('Password')
        el.clear()
        self.send_keys(el, cfg.site.bad_password)

    @Trace(log)
    def input_bad_username(self):
        el = self.find_named_element('UserName')
        el.clear()
        self.send_keys(el, cfg.site.bad_username)

    @Trace(log)
    def input_password(self):
        el = self.find_named_element('Password')
        el.clear()
        self.send_keys(el, cfg.site.password)

    @Trace(log)
    def input_username(self):
        el = self.find_named_element('UserName')
        el.clear()
        self.send_keys(el, cfg.site.username)

    @Trace(log)
    def click_login(self):
        self.click_named_element('LoginButton')

    def login_with_good_credentials(self):
        self.login(username=cfg.site.username, password=cfg.site.password)

    def login_no_username(self):
        self.login(password=cfg.site.password)

    def login_bad_username(self):
        self.login(username=cfg.site.bad_username, password=cfg.site.password)

    def login_no_password(self):
        self.login(username=cfg.site.username)

    def login_bad_password(self):
        self.login(username=cfg.site.username, password=cfg.site.bad_password)

    def login(self, username=None, password=None):
        if username is not None:
            el = self.find_named_element('UserName')
            el.clear()
            self.send_keys(el, username)
        if password is not None:
            el = self.find_named_element('Password')
            el.clear()
            self.send_keys(el, password)
        self.click_named_element('LoginButton')

    def wait_for_invalid_login_alert(self):
        assert self.element_is_present('InvalidLoginAlert')


login_view = LoginView()
