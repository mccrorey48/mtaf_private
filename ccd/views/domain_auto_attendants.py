import lib.logging_esi as logging

from ccd.views.domain import DomainView

log = logging.get_logger('esi.domain_auto_attendants_view')


class DomainAutoAttendantsView(DomainView):

    def __init__(self):
        super(DomainAutoAttendantsView, self).__init__()
        self.view_name = "domain_auto_attendants"
        self.page_title = "Manager Portal - Auto Attendants"

domain_auto_attendants_view = DomainAutoAttendantsView()
