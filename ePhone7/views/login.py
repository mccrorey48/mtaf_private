from lib.common.configure import cfg
from lib.android.actions import Actions
from lib.common.wrappers import Trace
import lib.common.logging_esi as logging
log = logging.get_logger('esi.login_view')


class LoginView:

    @Trace(log)
    def __init__(self):
        self.actions = Actions(self)

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
        self.actions.find_element_by_key('Username').set_text(login_id)
        self.actions.find_element_by_key('Password').set_text(passwd)
        self.actions.click_element_by_key('Login')
        self.actions.wait_for_condition_true(lambda: remote.current_activity == '.activities.MainViewActivity')

login_view = LoginView()
