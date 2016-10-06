import lib.common.logging_esi as logging
from lib.common.wrappers import Trace
from ccd.views.reseller import ResellerView
from ccd.utils.configure import cfg

log = logging.get_logger('esi.reseller_home_view')


class ResellerHomeView(ResellerView):

    def __init__(self):
        super(ResellerHomeView, self).__init__()
        self.view_name = "reseller home"
        self.page_title = "Manager Portal - Home"

    @Trace(log)
    def goto_test_domain_quick(self):
        self.filter_dropdown_and_click_result_by_link_text("DomainQuickLaunch", cfg.site["TestDomainMin"],
                                                                   cfg.site["TestDomainExtended"])
        self.find_element_by_key("DomainMessage")

reseller_home_view = ResellerHomeView()
