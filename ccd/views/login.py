from mtaf import mtaf_logging

from ccd.utils.configure import cfg
from ccd.views.base import BaseView
from mtaf.decorators import Trace

log = mtaf_logging.get_logger('mtaf.login_view')


class LoginView(BaseView):

    locators = {
        "LoginButton": {"by": "xpath", "value": "//input[@value='Log In']"},
        "Password": {"by": "id", "value": "LoginPassword"},
        "PasswordAlert": {"by": "css selector", "value": ".alert"},
        "UserName": {"by": "id", "value": "LoginUsername"}
    }

    def __init__(self):
        super(LoginView, self).__init__()
        self.view_name = "login"
        self.page_title = "Manager Portal"

    @Trace(log)
    def input_bad_username(self):
        user_cfg = cfg.site['Users']['ResellerUser']
        username = '%s@%s' % (user_cfg['BadUserId'], user_cfg['DomainName'])
        self.find_named_element('UserName').send_keys(username)

    @Trace(log)
    def input_reseller_username(self):
        user_cfg = cfg.site['Users']['ResellerUser']
        username = '%s@%s' % (user_cfg['UserId'], user_cfg['DomainName'])
        self.find_named_element('UserName').send_keys(username)

    @Trace(log)
    def input_reseller_password(self):
        user_cfg = cfg.site['Users']['ResellerUser']
        password = user_cfg['Password']
        self.find_named_element('Password').send_keys(password)

    @Trace(log)
    def input_bad_password(self):
        user_cfg = cfg.site['Users']['ResellerUser']
        password = user_cfg['BadPassword']
        self.find_named_element('Password').send_keys(password)

    @Trace(log)
    def click_login(self):
        self.click_named_element('LoginButton')

    def login_with_good_credentials(self):
        user_cfg = cfg.site['Users']['ResellerUser']
        username = '%s@%s' % (user_cfg['UserId'], user_cfg['DomainName'])
        password = user_cfg['Password']
        self.login(username, password)

    def login_bad_password(self):
        user_cfg = cfg.site['Users']['ResellerUser']
        username = '%s@%s' % (user_cfg['UserId'], user_cfg['DomainName'])
        password = user_cfg['BadPassword']
        self.login(username, password)

    def login_no_password(self):
        user_cfg = cfg.site['Users']['ResellerUser']
        username = '%s@%s' % (user_cfg['UserId'], user_cfg['DomainName'])
        password = ''
        self.login(username, password)

    def login_bad_username(self):
        user_cfg = cfg.site['Users']['ResellerUser']
        username = '%s@%s' % (user_cfg['BadUserId'], user_cfg['DomainName'])
        password = user_cfg['Password']
        self.login(username, password)

    def login_no_username(self):
        user_cfg = cfg.site['Users']['ResellerUser']
        username = ''
        password = user_cfg['Password']
        self.login(username, password)

    def login(self, username, password):
        if len(username):
            self.find_named_element('UserName').send_keys(username)
        if len(password):
            self.find_named_element('Password').send_keys(password)
        self.click_named_element('LoginButton')

    def wait_for_invalid_login_alert(self, timeout=10):
        el = self.find_named_element("PasswordAlert", timeout)
        self.assert_element_text(elem=el, expected="Username or password is invalid. Please try again.",
                                 elem_name="alert")


login_view = LoginView()
