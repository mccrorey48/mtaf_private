from mtaf import mtaf_logging

from ccd.views.domain import DomainView

log =mtaf_logging.get_logger('mtaf.domain_time_frames_view')


class DomainTimeFramesView(DomainView):

    locators = {
        "TrashCanIconSub": {"by": "xpath", "value": "td[4]/a[2]"},
        "AddTimeFrame": {"by": "xpath", "value": "//div[@id='content']/div/div[3]/a"},
        "SaveButton": {"by": "id", "value": "tfSaveBtn"},
        "TimeframeAddForm": {"by": "id", "value": "TimeframeAddForm"},
        "TimeframeName": {"by": "id", "value": "TimeframeName"}
    }

    def __init__(self):
        super(DomainTimeFramesView, self).__init__()
        self.view_name = "domain_time_frames"
        self.page_title = "Manager Portal - Time Frames"

domain_time_frames_view = DomainTimeFramesView()
