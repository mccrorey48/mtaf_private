import lib.common.logging_esi as logging_esi
from ePhone7.utils.configure import cfg
from lib.android.actions import Actions
from lib.common.wrappers import Trace

log = logging_esi.get_logger('esi.user_view')


class BaseView(object):

    @Trace(log)
    def __init__(self):
        self.cfg = cfg
        self.actions = Actions(self)

base_view = BaseView()
