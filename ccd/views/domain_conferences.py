import lib.logging_esi as logging

from ccd.views.domain import DomainView

log = logging.get_logger('esi.domain_conferences_view')


class DomainConferencesView(DomainView):

    locators = {
        "DomainsTab": {"by": "id", "value": "nav-domains"},
        "InventoryTab": {"by": "id", "value": "nav-inventory"},
        "HomeTab": {"by": "id", "value": "nav-home-reseller"},
        "Logout": {"by": "id", "value": "logout"},
        "TrashCanIconSub": {"by": "xpath", "value": "td[7]/a[3]"},
        "ConfirmYes": {"by": "xpath", "value": "/html/body/div[2]/div[2]/div/a[1]"}
    }

    def __init__(self):
        super(DomainConferencesView, self).__init__()
        self.view_name = "domain_conferences"
        self.page_title = "Manager Portal - Conferences"

domain_conferences_view = DomainConferencesView()
