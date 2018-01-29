from mtaf import mtaf_logging
from mtaf.trace import Trace

from ePhone7.views.base_view import BaseView

log = mtaf_logging.get_logger('esi.app_intro_view')


class AppIntroView(BaseView):

    locators = {
        "Skip": {"by": "id", "value": "com.esi_estech.ditto:id/skip"}
    }

    def __init__(self):
        super(AppIntroView, self).__init__()
        self.png_file_base = 'tnc'
        BaseView.app_intro_view = self
        self.presence_element_names = ['Skip']

    @Trace(log)
    def skip_intro(self):
        self.click_named_element('Skip')
        self.wait_for_activity('.activities.MainViewActivity')

app_intro_view = AppIntroView()
