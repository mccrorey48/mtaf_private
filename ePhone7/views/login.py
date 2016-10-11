import lib.logging_esi as logging

from ePhone7.utils.configure import cfg
from ePhone7.views.base import BaseView
from lib.wrappers import Trace

log = logging.get_logger('esi.login_view')


class LoginView(BaseView):

    locators = {
        "Login": {"by": "id", "value": "com.esi_estech.ditto:id/login_button"},
        "Password": {"by": "id", "value": "com.esi_estech.ditto:id/login_password"},
        "Username": {"by": "id", "value": "com.esi_estech.ditto:id/login_username"}
    }

    @Trace(log)
    def __init__(self):
        super(LoginView, self).__init__()

    # def not_login_view(self):
    #     current_activity = remote.get_current_activity()
    #     print "current activity: " + current_activity
    #     return (current_activity != '.settings.ui.LoginActivity')

    # def not_login_activity(self):
    #     return remote.driver.current_activity != '.settings.ui.LoginActivity'

    @Trace(log)
    def login(self):
        acct_cfg = cfg.site['Accounts']['R2d2User']
        login_id = '%s@%s' % (acct_cfg['UserId'], acct_cfg['DomainName'])
        self.find_element_by_key('Username').set_text(login_id)
        self.find_element_by_key('Password').set_text(passwd)
        self.click_element_by_key('Login')
        failmsg = 'current activity is not .activities.MainViewActivity'
        testfn = lambda: self.current_activity == '.activities.MainViewActivity'
        self.wait_for_condition_true(testfn, failmsg)

login_view = LoginView()
