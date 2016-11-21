from ePhone7.utils.configure import cfg
from lib.softphone.softphone import Softphone


def get_softphone(user_name=None):
    if user_name is None:
        user_name = cfg.site["DefaultSoftphoneUser"]
    user_cfg = cfg.site['Users'][user_name]
    return Softphone(user_cfg)
