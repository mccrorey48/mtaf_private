import lib.common.logging_esi as logging
from lib.common.wrappers import Trace
from ccd.views.reseller import ResellerView
from ccd.utils.configure import cfg
from time import sleep

log = logging.get_logger('esi.reseller_home_view')


class ResellerHomeView(ResellerView):

    @Trace(log)
    def __init__(self):
        super(ResellerHomeView, self).__init__()
        self.version_info = None
        self.view_name = "reseller home"
        self.page_title = "Manager Portal - Home"

    @Trace(log)
    def goto_test_domain_quick(self):
        elem = self.actions.find_element_by_key("DomainQuickLaunch")
        sleep(1)
        elem.send_keys(cfg.site["TestDomainMin"])
        sleep(1)
        self.actions.send_tab_to_element(elem)
        self.actions.find_element_by_key("DomainMessage")

reseller_home_view = ResellerHomeView()
