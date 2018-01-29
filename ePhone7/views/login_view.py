from mtaf import mtaf_logging
from mtaf.trace import Trace

from ePhone7.config.configure import cfg
from ePhone7.views.base_view import BaseView

log = mtaf_logging.get_logger('esi.login_view')


class LoginView(BaseView):

    locators = {
        "Login": {"by": "id", "value": "com.esi_estech.ditto:id/login_button"},
        "Password": {"by": "id", "value": "com.esi_estech.ditto:id/login_password"},
        "Username": {"by": "id", "value": "com.esi_estech.ditto:id/login_username"}
    }

    def __init__(self):
        super(LoginView, self).__init__()
        self.png_file_base = 'login'
        self.last_activity = None
        BaseView.login_view = self
        self.presence_element_names = ['Login']

    @Trace(log)
    def login(self):
        acct_cfg = cfg.site['Users']['R2d2User']
        login_id = '%s@%s' % (acct_cfg['UserId'], acct_cfg['DomainName'])
        passwd = acct_cfg['PhonePassword']
        self.find_named_element('Username').set_text(login_id)
        self.find_named_element('Password').set_text(passwd)
        self.click_named_element('Login')
        self.wait_for_activity('.settings.ui.TermsAndConditionsScreen')

login_view = LoginView()

