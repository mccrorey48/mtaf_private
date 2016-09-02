import lib.common.logging_esi as logging
from ccd.utils.configure import cfg
from lib.chrome.actions import Actions
from lib.common.wrappers import Trace

log = logging.get_logger('esi.base_view')


class BaseView(object):

    @Trace(log)
    def __init__(self):
        self.cfg = cfg
        self.actions = Actions(self)
        self.view_name = "Not Initialized"
        self.page_title = "Not Initialized"
        self.actions.open_browser()

    @Trace(log)
    def get_portal_url(self):
        portal_url = cfg.site['PortalUrl']
        self.actions.get_url(portal_url)

    @Trace(log)
    def open_browser(self):
        self.actions.open_browser()

    @Trace(log)
    def close_browser(self):
        self.actions.close_browser()

    @Trace(log)
    def wait_for_page_title(self, timeout=20):

        def condition_fn():
            return self.actions.get_title() == self.page_title

        def msg_fn():
            return ('wrong page title for %s view after %s seconds, expect "%s", actual "%s"'
                          % (self.view_name, timeout, self.page_title, self.actions.get_title()))

        self.actions.wait_for_condition_true(condition_fn, msg_fn, timeout)

base_view = BaseView()
