import lib.logging_esi as logging

from ePhoneGoAndroid.views.base import BaseView
from lib.wrappers import Trace

log = logging.get_logger('esi.storage_view')


class StorageView(BaseView):

    locators = {
        "ActionBarText": {"by": "xpath", "value": "//fl[1]/vg/tv", "text": "Internal Storage"},
        "Apps": {"by": "id", "value": "android:id/title", "text": "Apps"},
        "ePhoneGo": {"by": "id", "value": "android:id/title", "text": "ePhoneGO"},
        "ClearData": {"by": "id", "value": "com.android.settings:id/button", "text": "Clear data"},
        "Delete": {"by": "id", "value": "android:id/button1", "text": "DELETE"}
    }

    def __init__(self):
        super(StorageView, self).__init__()


storage_view = StorageView()
