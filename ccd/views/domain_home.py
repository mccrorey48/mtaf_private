import lib.logging_esi as logging

from ccd.views.domain import DomainView

log = logging.get_logger('esi.domain_home_view')


class DomainHomeView(DomainView):

    def __init__(self):
        super(DomainHomeView, self).__init__()
        self.view_name = "domain_home"
        self.page_title = "Manager Portal - Home"

domain_home_view = DomainHomeView()
