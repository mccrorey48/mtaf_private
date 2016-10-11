import lib.logging_esi as logging

from ccd.views.reseller import ResellerView

log = logging.get_logger('esi.reseller_inventory_view')


class ResellerInventoryView(ResellerView):

    def __init__(self):
        super(ResellerInventoryView, self).__init__()
        self.view_name = "reseller inventory"
        self.page_title = "Manager Portal - Inventory"

reseller_inventory_view = ResellerInventoryView()
