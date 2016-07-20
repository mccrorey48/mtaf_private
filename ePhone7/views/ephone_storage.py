from ePhone7.views.app_storage import AppStorageView
from lib.android.actions import Actions
from lib.common.wrappers import Trace
import lib.common.logging_esi as logging
log = logging.get_logger('esi.ephone_storage_view')


class EphoneStorageView(AppStorageView):

    @Trace(log)
    def __init__(self):
        AppStorageView.__init__(self)
        self.actions = Actions(self)

ephone_storage_view = EphoneStorageView()
