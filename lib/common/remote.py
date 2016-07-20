from appium import webdriver
from lib.common.configure import cfg
import lib.common.logging_esi as logging
from lib.common.user_exception import UserException as Ux
from time import time

log = logging.get_logger('esi.remote')


class Remote:

    viewName = 'not initialized'
    caps_tag = 'not initialized'
    current_implicit_wait = None
    current_activity = None
    driver = None
    default_timeout = 10
    timeout = None

    def __init__(self, timeout=default_timeout):
        # if cfg.site['Mock']:
        #     self.driver = MockDriver()
        # else:
        #     self.update_remote('nolaunch')
        self.timeout = timeout
        self.update_remote('nolaunch')

    def update_remote(self, caps_tag, timeout=cfg.site['DefaultTimeout']):
        # if not cfg.site['Mock']:
        if caps_tag != self.caps_tag:
            if self.caps_tag != 'not initialized':
                self.driver.quit()
            self.driver = webdriver.Remote(cfg.site["URL"], cfg.caps[caps_tag])
            self.caps_tag = caps_tag
            self.driver.implicitly_wait(timeout)
            self.current_implicit_wait = timeout
            self.current_activity = self.driver.current_activity
            log.debug("self.caps_tag = %s, self.current_activity = %s" % (self.caps_tag, self.current_activity))

    def get_current_activity_tag(self, state):
        activity_tags_by_state = {
            'start': {
                '.settings.ui.LoginActivity': 'login',
                '.settings.ui.TermsAndConditionsScreen': 'tnc',
                '.SubSettings': 'settings',
                '.activities.MainViewActivity': 'main'
            },
            'test_for_tnc': {
                '.settings.ui.TermsAndConditionsScreen': 'tnc',
                '.settings.ui.LoginActivity': 'tnc',
                '.activities.MainViewActivity': 'main'
            },
            'logged_in_expect_tnc': {
                '.settings.ui.TermsAndConditionsScreen': 'tnc'
            },
            'logged_in_after_clear': {
                '.activities.MainViewActivity': 'main'
            },
            'tnc_accepted': {
                '.activities.MainViewActivity': 'main'
            },
            'hard_logged_out': {
                '.settings.ui.LoginActivity': 'login'
            }
        }
        if state not in activity_tags_by_state:
            raise Ux('program error - state %s not in activity_tags_by_state' % state)
        if self.current_activity in activity_tags_by_state[state]:
            return activity_tags_by_state[state][self.current_activity]
        else:
            raise Ux('unknown activity for state %s: %s' % (state, self.current_activity))

    def find_element_with_timeout(self, method, value, parent=None, timeout=10):
        if method == 'xpath':
            if parent is None:
                finder_fn = self.driver.find_elements_by_xpath
            else:
                finder_fn = parent.find_elements_by_xpath
        elif method == 'id':
            if parent is None:
                finder_fn = self.driver.find_elements_by_id
            else:
                finder_fn = parent.find_elements_by_id
        elif method == 'accessibility id':
            if parent is None:
                finder_fn = self.driver.find_elements_by_accessibility_id
            else:
                finder_fn = parent.find_elements_by_accessibility_id
        else:
            raise Ux("Unknown finder method %s" % method)
        start_time = time()
        while time() - start_time < timeout:
            elems = finder_fn(value)
            if len(elems) > 1:
                raise Ux("Multiple elements match %s = %s, parent = %s" % (method, value, parent))
            if len(elems) == 1:
                return elems[0]
        raise Ux("No matching elements found with %s = %s, timeout = %s, parent = %s" % (method, value, timeout, parent))

remote = Remote()
