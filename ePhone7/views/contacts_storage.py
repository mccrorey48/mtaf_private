import lib.logging_esi as logging

from ePhone7.views.app_storage import AppStorageView
from lib.wrappers import Trace

log = logging.get_logger('esi.contacts_storage_view')


class ContactsStorageView(AppStorageView):

    locators = {
        "ClearData": {"by": "zpath", "value": "//bt[contains(@text,'Clear data')]"},
        "DataSize": {"by": "id", "value": "com.android.settings:id/data_size_text"},
        "Ok": {"by": "zpath", "value": "//bt[contains(@text,'OK')]"},
        "Settings": {"by": "id", "value": "android:id/home"},
        "Apps": {"by": "id", "value": "android:id/home"}
    }

    @Trace(log)
    def __init__(self):
        super(ContactsStorageView, self).__init__()

contacts_storage_view = ContactsStorageView()
