from ePhone7.utils.configure import cfg
from lib.softphone.simple_pj import Softphone


def get_softphone(user_name=None):
    if user_name is None:
        user_name = cfg.site["DefaultSoftphoneUser"]
    user_cfg = cfg.site['Users'][user_name]
    uri = "sip:%s@%s" % (user_cfg['UserId'], user_cfg['DomainName'])
    proxy = user_cfg['Proxy']
    password = user_cfg['PhonePassword']
    null_snd = cfg.site['NullSound']
    dns_list = cfg.site['DnsList']
    tcp = cfg.site['UseTcp']
    return Softphone(uri, proxy, password, null_snd, dns_list, tcp)
