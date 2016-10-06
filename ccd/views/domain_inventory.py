import lib.common.logging_esi as logging
from lib.common.wrappers import Trace
from ccd.views.domain import DomainView

log = logging.get_logger('esi.domain_inventory_view')


class DomainInventoryView(DomainView):

    def __init__(self):
        super(DomainInventoryView, self).__init__()
        self.view_name = "domain_inventory"
        self.page_title = "Manager Portal - Inventory"

domain_inventory_view = DomainInventoryView()
