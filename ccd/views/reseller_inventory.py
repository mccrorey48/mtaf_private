import lib.common.logging_esi as logging
from lib.common.wrappers import Trace
from ccd.views.reseller import ResellerView

log = logging.get_logger('esi.reseller_inventory_view')


class ResellerInventoryView(ResellerView):

    @Trace(log)
    def __init__(self):
        super(ResellerInventoryView, self).__init__()
        self.version_info = None
        self.view_name = "reseller inventory"
        self.page_title = "Manager Portal - Inventory"

reseller_inventory_view = ResellerInventoryView()
