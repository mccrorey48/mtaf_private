import lib.common.logging_esi as logging
from lib.common.wrappers import Trace
from ccd.views.reseller import ResellerView

log = logging.get_logger('esi.reseller_home_view')


class ResellerHomeView(ResellerView):

    @Trace(log)
    def __init__(self):
        super(ResellerHomeView, self).__init__()
        self.version_info = None
        self.view_name = "reseller home"
        self.page_title = "Manager Portal - Home"

reseller_home_view = ResellerHomeView()
