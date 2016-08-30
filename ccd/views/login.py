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
        self.actions = Actions(self, cfg)

    @Trace(log)
    def login(self):
        version_re = re.compile('.*<!-- ESI Cloud Communication Dashboard (v\.\d+\.\d+\.\d+) build (\d+) Date: ([^-]*) -- (\S*)', re.MULTILINE | re.DOTALL)
        portal_url = cfg.site['PortalUrl']
        user_cfg = cfg.site['Accounts']['ResellerUser']
        username = '%s@%s' % (user_cfg['UserId'], user_cfg['DomainName'])
        password = user_cfg['Password']
        self.actions.driver.get(portal_url)
        self.actions.driver.find_element_by_id('LoginUsername').send_keys(username)
        self.actions.driver.find_element_by_id('LoginPassword').send_keys(password)
        self.actions.driver.find_element_by_id('loginBtn').click()
        sleep(10)
        source = self.actions.driver.page_source
        m = version_re.match(source)
        if m:
            print 'version %s' % m.group(1)
            print 'build %s' % m.group(2)
            print 'date %s' % m.group(3)
            print 'time %s' % m.group(4)

login_view = LoginView()
