import lib.common.logging_esi as logging_esi
from ePhone7.utils.configure import cfg
from lib.android.actions import Actions

log = logging_esi.get_logger('esi.user_view')


class BaseView(Actions):

    def __init__(self):
        super(BaseView, self).__init__()
        self.cfg = cfg

    def __str__(self):
        return self.__class__().__name__

base_view = BaseView()
