import lib.common.logging_esi as logging
from ccd.utils.configure import cfg
from lib.chrome.actions import Actions
from lib.common.wrappers import Trace
import re
from time import sleep

log = logging.get_logger('esi.login_view')


class LoginView:

    @Trace(log)
    def __init__(self):
        self.actions = Actions(self)

    @Trace(log)
    def login_with_good_credentials(self):
        user_cfg = cfg.site['Accounts']['ResellerUser']
        username = '%s@%s' % (user_cfg['UserId'], user_cfg['DomainName'])
        password = user_cfg['Password']
        self.login(username, password)

    def login_with_bad_username(self):
        user_cfg = cfg.site['Accounts']['ResellerUser']
        username = '%s@%s' % (user_cfg['UserId'], user_cfg['DomainName'])
        password = user_cfg['Password']
        self.login(username, password)

    def login(self, username, password):
        portal_url = cfg.site['PortalUrl']
        self.actions.driver.get(portal_url)
        if len(username):
            self.actions.driver.find_element_by_id('LoginUsername').send_keys(username)
        if len(password):
            self.actions.driver.find_element_by_id('LoginPassword').send_keys(password)
        self.actions.driver.find_element_by_id('loginBtn').click()

login_view = LoginView()
