import lib.logging_esi as logging

from ePhone7.views.app_storage import AppStorageView
from lib.wrappers import Trace

log = logging.get_logger('esi.ephone_storage_view')


class EphoneStorageView(AppStorageView):

    @Trace(log)
    def __init__(self):
        super(EphoneStorageView, self).__init__()

ephone_storage_view = EphoneStorageView()
