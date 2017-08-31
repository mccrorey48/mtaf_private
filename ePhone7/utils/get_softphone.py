from ePhone7.config.configure import cfg
from lib.softphone.simple_pj import SoftphoneManager

softphone_manager = SoftphoneManager()


def get_softphone(user_name='default', user_group='Users'):
    if user_name == 'default':
        user_name = cfg.site['DefaultSoftphoneUser']
    user_cfg = cfg.site[user_group][user_name]
    uri = "sip:%s@%s" % (user_cfg['UserId'], user_cfg['DomainName'])
    proxy = user_cfg['Proxy']
    password = user_cfg['PhonePassword']
    null_snd = cfg.site['NullSound']
    dns_list = cfg.site['DnsList']
    tcp = cfg.site['UseTcp']
    return softphone_manager.get_softphone(uri, proxy, password, null_snd, dns_list, tcp)


def delete_softphone(softphone):
    softphone_manager.delete_softphone(softphone)
