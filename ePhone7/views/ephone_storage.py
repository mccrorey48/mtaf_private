import lib.logging_esi as logging

from ePhone7.views.app_storage import AppStorageView
from lib.wrappers import Trace

log = logging.get_logger('esi.ephone_storage_view')


class EphoneStorageView(AppStorageView):

    locators = {
        "ClearData": {"by": "zpath", "value": "//bt[contains(@text,'Clear data')]"},
        "DataSize": {"by": "id", "value": "com.android.settings:id/data_size_text"},
        "Ok": {"by": "zpath", "value": "//bt[contains(@text,'OK')]"},
        "Apps": {"by": "id", "value": "android:id/home"}
    }

    @Trace(log)
    def __init__(self):
        super(EphoneStorageView, self).__init__()

ephone_storage_view = EphoneStorageView()
