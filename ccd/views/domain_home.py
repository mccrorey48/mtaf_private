from mtaf import mtaf_logging

from ccd.views.domain import DomainView

log = mtaf_logging.get_logger('mtaf.domain_home_view')


class DomainHomeView(DomainView):

    def __init__(self):
        super(DomainHomeView, self).__init__()
        self.view_name = "domain_home"
        self.page_title = "Manager Portal - Home"


domain_home_view = DomainHomeView()
