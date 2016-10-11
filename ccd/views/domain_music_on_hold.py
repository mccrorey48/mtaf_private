import lib.logging_esi as logging

from ccd.views.domain import DomainView

log = logging.get_logger('esi.domain_music_on_hold_view')


class DomainMusicOnHoldView(DomainView):

    def __init__(self):
        super(DomainMusicOnHoldView, self).__init__()
        self.view_name = "domain_music_on_hold"
        self.page_title = "Manager Portal - Music On Hold"

domain_music_on_hold_view = DomainMusicOnHoldView()
