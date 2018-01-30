from mtaf import mtaf_logging

from ccd.views.domain import DomainView

log =mtaf_logging.get_logger('mtaf.domain_conferences_view')


class DomainConferencesView(DomainView):

    locators = {
        "DomainsTab": {"by": "id", "value": "nav-domains"},
        "InventoryTab": {"by": "id", "value": "nav-inventory"},
        "HomeTab": {"by": "id", "value": "nav-home-reseller"},
        "Logout": {"by": "id", "value": "logout"},
        "TrashCanIconSub": {"by": "xpath", "value": "td[7]/a[3]"}
    }

    def __init__(self):
        super(DomainConferencesView, self).__init__()
        self.view_name = "domain_conferences"
        self.page_title = "Manager Portal - Conferences"

domain_conferences_view = DomainConferencesView()
