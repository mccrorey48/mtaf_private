import datetime
from time import time
from lib.wrappers import Trace
import lib.logging_esi as logging
from ePhone7.config.configure import cfg
from lib.microservices import Microservices

log = logging.get_logger('esi.get_vmids')
__all__ = ['get_vmids', 'VvmMicroservice']

default_fields = ['dateRecorded', 'duration', 'timeZone', 'vmid', 'callerName', 'callerNumber', 'mediaSize', ]


def get_user_cfg(username):
    user_cfg = cfg.site['Users'][username]
    oauth_url = cfg.site["OauthURL"] + "/login"
    login_name = user_cfg['UserId'] + '@' + user_cfg['DomainName']
    password = user_cfg['AccountPassword']
    return login_name, password


class VvmMicroservice(object):
    def __init__(self, username='R2d2User'):
        self.username = username
        self.oauth_start_time = None
        self.microservices = None

    def start_microservice(self, username):
        tries = 2
        while True:
            tries -= 1
            try:
                self.oauth_start_time = time()
                return Microservices(*get_user_cfg(username))
            except ValueError:
                if tries > 0:
                    log.warn("ValueError instantiating Microservices - retrying")
                else:
                    raise

    def get_microservices(self):
        if self.oauth_start_time is None or time() - self.oauth_start_time > 3500:
            self.microservices = self.start_microservice(self.username)
        return self.microservices

    def get_vm_metadata(self, category, fields=default_fields):
        category = category.lower()
        microservices = self.get_microservices()
        mds = microservices.get_vm_metadata(category.lower()).json()
        for md in mds:
            log.debug('vm metadata: %s' % md)
        return [{field: str(md[field]) for field in fields} for md in mds]

    def delete_one_vm(self, category, vmid):
        category = category.lower()
        microservices = self.get_microservices()
        mds = microservices.delete_one_vm(category, vmid)

    def undelete_one_vm(self, vmid):
        microservices = self.get_microservices()
        microservices.undelete_one_vm(vmid)

    def get_vm_count(self, category):
        category = category.lower()
        microservices = self.get_microservices()
        return microservices.get_vm_count(category).json()


@Trace(log)
def get_vmids(username, category):
    vvm_microservice = VvmMicroservice(username)
    mds = vvm_microservice.get_vm_metadata(category)
    return [md['vmid'] for md in mds]
