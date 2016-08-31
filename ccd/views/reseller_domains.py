import lib.common.logging_esi as logging
from lib.common.wrappers import Trace
from ccd.views.reseller import ResellerView

log = logging.get_logger('esi.reseller_domains_view')


class ResellerDomainsView(ResellerView):

    @Trace(log)
    def __init__(self):
        super(ResellerDomainsView, self).__init__()
        self.version_info = None
        self.view_name = "reseller domains"
        self.page_title = "Manager Portal - Domains"

reseller_domains_view = ResellerDomainsView()
