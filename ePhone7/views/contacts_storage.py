import lib.logging_esi as logging

from ePhone7.views.app_storage import AppStorageView
from lib.wrappers import Trace

log = logging.get_logger('esi.contacts_storage_view')


class ContactsStorageView(AppStorageView):

    @Trace(log)
    def __init__(self):
        super(ContactsStorageView, self).__init__()

contacts_storage_view = ContactsStorageView()
