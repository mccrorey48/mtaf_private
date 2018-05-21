from mtaf import mtaf_logging

from ePhoneGoAndroid.views.base import BaseView
from lib.wrappers import Trace

log = mtaf_logging.get_logger('mtaf.login_view')


class LoginView(BaseView):

    locators = {
        "AttentionAlertMessage": {"by": "id", "value": "android:id/message", "text": "For ESI ePhoneGo to work"},
        "AttentionOkButton": {"by": "id", "value": "android:id/button1"},
        "PhonePermissionAlertTitle": {"by": "id", "value": "com.android.packageinstaller:id/permission_message",
                                      "text": "Allow ESI ePhoneGO to make and manage phone calls?"},
        "PermissionAllowButton": {"by": "id", "value": "com.android.packageinstaller:id/permission_allow_button",
                                  "text": "Allow"},
        "RecordAudioAlertMessage": {"by": "id", "value": "com.android.packageinstaller:id/permission_message",
                                    "text": "Allow ESI ePhoneGO to record audio?"},
        "AccessContactsAlertMessage": {"by": "id", "value": "com.android.packageinstaller:id/permission_message",
                                       "text": "Allow ESI ePhoneGO to access your contacts?"},
        "AccessMediaAlertMessage": {"by": "id", "value": "com.android.packageinstaller:id/permission_message",
                                    "text": "Allow ESI ePhoneGO to access photos, media, and files on your device?"},
        "AccessLocationAlertMessage": {"by": "id", "value": "com.android.packageinstaller:id/permission_message",
                                       "text": "Allow ESI ePhoneGO to access this device's location?"},
        "FunctionalityAlertMessage": {"by": "id", "value": "android:id/message",
                                      "text": "To use the full functionality of ESI ePhoneGO"},
        "BatteryUsageAlertMessage": {"by": "id", "value": "android:id/message",
                                     "text": "ESI ePhoneGO will be able to run in the background"},
        "BatteryUsageYesButton": {"by": "id", "value": "android:id/button1"},
        "Accept": {"by": "id", "value": "com.esi_estech.ditto:id/TnC_checkBox_continue"},
        "Continue": {"by": "id", "value": "com.esi_estech.ditto:id/TnC_continueBtn"},
        "Login": {"by": "id", "value": "com.esi_estech.ditto:id/login_button"}
    }

    def __init__(self):
        super(LoginView, self).__init__()
        self.png_file_base = 'login'

login_view = LoginView()
