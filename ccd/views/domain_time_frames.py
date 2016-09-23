import lib.common.logging_esi as logging
from lib.common.wrappers import Trace
from ccd.views.domain import DomainView

log = logging.get_logger('esi.domain_time_frames_view')


class DomainTimeFramesView(DomainView):

    @Trace(log)
    def __init__(self):
        super(DomainTimeFramesView, self).__init__()
        self.view_name = "domain_time_frames"
        self.page_title = "Manager Portal - Time Frames"

domain_time_frames_view = DomainTimeFramesView()
