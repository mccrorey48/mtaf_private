import lib.logging_esi as logging

from ccd.utils.configure import cfg
from ccd.views.reseller import ResellerView
from lib.wrappers import Trace

log = logging.get_logger('esi.reseller_home_view')


class ResellerHomeView(ResellerView):

    locators = {
        "DomainQuickLaunch": {"by": "id", "value": "domains"}
    }

    def __init__(self):
        super(ResellerHomeView, self).__init__()
        self.view_name = "reseller home"
        self.page_title = "Manager Portal - Home"

    @Trace(log)
    def goto_test_domain_quick(self):
        self.filter_dropdown_and_click_result_by_link_text("DomainQuickLaunch", cfg.site["TestDomainMin"],
                                                           cfg.site["TestDomainExtended"])

reseller_home_view = ResellerHomeView()
