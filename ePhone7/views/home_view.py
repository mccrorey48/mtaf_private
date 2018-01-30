from mtaf import mtaf_logging
from ePhone7.views.user_view import UserView

log = mtaf_logging.get_logger('mtaf.contacts_view')


class HomeView(UserView):

    locators = {
        "HomeScreenLogo": {"by": "id", "value": "com.esi_estech.ditto:id/home_screen_company_logo"},
    }

    def __init__(self):
        super(HomeView, self).__init__()
        self.png_file_base = 'home'
        self.presence_element_names = ['HomeScreenLogo']


home_view = HomeView()
