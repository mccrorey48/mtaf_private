import lib.common.logging_esi as logging
from ccd.utils.configure import cfg
from lib.common.wrappers import Trace
from ccd.views.base import BaseView

log = logging.get_logger('esi.login_view')


class LoginView(BaseView):

    @Trace(log)
    def __init__(self):
        super(LoginView, self).__init__()
        self.view_name = "login"
        self.page_title = "Manager Portal"

    @Trace(log)
    def login_with_good_credentials(self):
        user_cfg = cfg.site['Accounts']['ResellerUser']
        username = '%s@%s' % (user_cfg['UserId'], user_cfg['DomainName'])
        password = user_cfg['Password']
        self.login(username, password)

    def login_bad_password(self):
        user_cfg = cfg.site['Accounts']['ResellerUser']
        username = '%s@%s' % (user_cfg['UserId'], user_cfg['DomainName'])
        password = user_cfg['BadPassword']
        self.login(username, password)

    def login_no_password(self):
        user_cfg = cfg.site['Accounts']['ResellerUser']
        username = '%s@%s' % (user_cfg['UserId'], user_cfg['DomainName'])
        password = ''
        self.login(username, password)

    def login_bad_username(self):
        user_cfg = cfg.site['Accounts']['ResellerUser']
        username = '%s@%s' % (user_cfg['BadUserId'], user_cfg['DomainName'])
        password = user_cfg['Password']
        self.login(username, password)

    def login_no_username(self):
        user_cfg = cfg.site['Accounts']['ResellerUser']
        username = ''
        password = user_cfg['Password']
        self.login(username, password)

    def login(self, username, password):
        if len(username):
            self.actions.find_element_by_key('UserName').send_keys(username)
        if len(password):
            self.actions.find_element_by_key('Password').send_keys(password)
        self.actions.click_element_by_key('LoginButton')

    def wait_for_password_alert(self, timeout=10):
        el = self.actions.find_element_by_key("PasswordAlert", timeout)
        self.actions.assert_element_text(elem=el, expected="Username or password is invalid. Please try again.",
                                         elem_name="alert")

login_view = LoginView()
