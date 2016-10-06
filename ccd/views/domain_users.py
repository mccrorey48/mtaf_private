import lib.common.logging_esi as logging
from lib.common.wrappers import Trace
from ccd.views.domain import DomainView

log = logging.get_logger('esi.domain_music_on_hold_view')


class DomainUsersView(DomainView):

    def __init__(self):
        super(DomainUsersView, self).__init__()
        self.view_name = "domain_music_on_hold"
        self.page_title = "Manager Portal - Users"

domain_users_view = DomainUsersView()
