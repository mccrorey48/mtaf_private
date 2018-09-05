from mtaf.trace import Trace
from ePhone7.config.configure import cfg
from microservices.microservices import get_microservices
from mtaf import mtaf_logging

log = mtaf_logging.get_logger('mtaf.vvm_usvc')
__all__ = ['get_e7_microservices', 'get_vmids']


@Trace(log)
def get_e7_microservices(username):
    user_cfg = cfg.site['Users'][username]
    oauth_url = cfg.site["OauthURL"] + "/login"
    login_name = user_cfg['UserId'] + '@' + user_cfg['DomainName']
    password = user_cfg['AccountPassword']
    return get_microservices(login_name, password)


def get_vmids(username, category):
    return [item['vmid'] for item in get_e7_microservices(username).get_vm_metadata(category)]


