from mtaf import mtaf_logging

from ccd.views.domain import DomainView

log = mtaf_logging.get_logger('mtaf.domain_call_queues_view')


class DomainCallQueuesView(DomainView):

    def __init__(self):
        super(DomainCallQueuesView, self).__init__()
        self.view_name = "domain_call_queues"
        self.page_title = "Manager Portal - Call Queues"


domain_call_queues_view = DomainCallQueuesView()
