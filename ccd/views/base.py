import lib.common.logging_esi as logging
from ccd.utils.configure import cfg
from lib.chrome.actions import Actions
from lib.common.wrappers import Trace

log = logging.get_logger('esi.base_view')


class BaseView(Actions):

    def __init__(self):
        self.cfg = cfg
        self.page_title = 'Page title not initialized'
        super(BaseView, self).__init__()
        self.open_browser()

    def get_portal_url(self):
        self.get_url(cfg.site['PortalUrl'])


    @Trace(log)
    def wait_for_page_title(self):
        self.wait_for_title(self.page_title, timeout=15)

base_view = BaseView()
