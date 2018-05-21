from mtaf import mtaf_logging

from ccd.views.domain import DomainView

log = mtaf_logging.get_logger('mtaf.domain_locations_view')


class DomainLocationsView(DomainView):

    def __init__(self):
        super(DomainLocationsView, self).__init__()
        self.view_name = "domain_locations"
        self.page_title = "Manager Portal - Locations"


domain_locations_view = DomainLocationsView()
