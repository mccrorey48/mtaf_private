import lib.logging_esi as logging

from ccd.views.domain import DomainView

log = logging.get_logger('esi.domain_conferences_view')


class DomainConferencesView(DomainView):

    def __init__(self):
        super(DomainConferencesView, self).__init__()
        self.view_name = "domain_conferences"
        self.page_title = "Manager Portal - Conferences"

domain_conferences_view = DomainConferencesView()
