from time import time, sleep

import lib.logging_esi as logging
from ePhone7.config.configure import cfg
from ePhone7.utils.get_softphone import get_softphone
from ePhone7.views.user_view import UserView
from lib.user_exception import UserException as Ux
from lib.wrappers import Trace
from lib.filters import get_filter

log = logging.get_logger('esi.contacts_view')


class HomeView(UserView):

    locators = {
        "HomeScreenLogo": {"by": "id", "value": "com.esi_estech.ditto:id/home_screen_company_logo"},
    }

    def __init__(self):
        super(HomeView, self).__init__()
        self.png_file_base = 'home'
        self.presence_element_names = ['HomeScreenLogo']


home_view = HomeView()
