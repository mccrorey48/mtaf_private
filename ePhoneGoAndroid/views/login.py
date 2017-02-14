import lib.logging_esi as logging

from ePhoneGoAndroid.views.base import BaseView
from lib.wrappers import Trace

log = logging.get_logger('esi.login_view')


class LoginView(BaseView):

    locators = {
        "Accept": {"by": "id", "value": "com.esi_estech.ditto:id/TnC_checkBox_continue"},
        "AttentionAlertTitle": {"by": "id", "value": "android:id/alertTitle", "text": "Attention"},
        "AttentionOkButton": {"by": "id", "value": "android:id/button1"},
        "BatteryUsageAlertTitle": {"by": "id", "value": "android:id/alertTitle", "text": "Ignore battery optimizations?"},
        "BatteryUsageYesButton": {"by": "id", "value": "android:id/button1"},
        "Continue": {"by": "id", "value": "com.esi_estech.ditto:id/TnC_continueBtn"},
        "Login": {"by": "id", "value": "com.esi_estech.ditto:id/login_button"},
        "PhonePermissionAlertTitle": {"by": "id", "value": "com.android.packageinstaller:id/permission_message",
                                      "text": "Allow ESI ePhoneGO to make and manage phone calls?"},
        "PermissionAllowButton": {"by": "id", "value": "com.android.packageinstaller:id/permission_allow_button"},
        "RecordAudioAlertTitle": {"by": "id", "value": "com.android.packageinstaller:id/permission_message",
                                  "text": "Allow ESI ePhoneGO to record audio?"}
    }

    def __init__(self):
        super(LoginView, self).__init__()
        self.png_file_base = 'login'

login_view = LoginView()
