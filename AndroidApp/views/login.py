import lib.mtaf_logging as logging
from AndroidApp.views.base import BaseView

log = logging.get_logger('mtaf.login_view')


class LoginView(BaseView):

    locators = {
        "Login": {"by": "id", "value": "com.foo.bar:id/login_button"}
    }

    def __init__(self):
        super(LoginView, self).__init__()
        self.png_file_base = 'login'


login_view = LoginView()
