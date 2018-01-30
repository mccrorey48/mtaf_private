from mtaf import mtaf_logging

from ccd.views.reseller import ResellerView

log =mtaf_logging.get_logger('mtaf.reseller_inventory_view')


class ResellerInventoryView(ResellerView):

    def __init__(self):
        super(ResellerInventoryView, self).__init__()
        self.view_name = "reseller inventory"
        self.page_title = "Manager Portal - Inventory"

reseller_inventory_view = ResellerInventoryView()
