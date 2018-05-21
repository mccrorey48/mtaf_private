from mtaf import mtaf_logging

from ccd.views.domain import DomainView

log = mtaf_logging.get_logger('mtaf.domain_inventory_view')


class DomainInventoryView(DomainView):

    def __init__(self):
        super(DomainInventoryView, self).__init__()
        self.view_name = "domain_inventory"
        self.page_title = "Manager Portal - Inventory"


domain_inventory_view = DomainInventoryView()
