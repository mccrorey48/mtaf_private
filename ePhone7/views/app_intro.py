import lib.logging_esi as logging

from ePhone7.views.base import BaseView
from lib.wrappers import Trace

log = logging.get_logger('esi.app_intro_view')


class AppIntroView(BaseView):

    locators = {
        "Skip": {"by": "id", "value": "com.esi_estech.ditto:id/skip"}
    }

    def __init__(self):
        super(AppIntroView, self).__init__()
        self.png_file_base = 'tnc'

    @Trace(log)
    def skip_intro(self):
        self.click_element_by_key('Skip')
        self.wait_for_activity('.activities.MainViewActivity')

app_intro_view = AppIntroView()
