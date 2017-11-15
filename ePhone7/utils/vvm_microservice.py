import datetime

from lib.wrappers import Trace
import lib.logging_esi as logging
from ePhone7.config.configure import cfg
from lib.microservices import Microservices

log = logging.get_logger('esi.get_vmids')
__all__ = ['get_vmids', 'get_vm_metadata', 'get_age_minutes']

default_fields = ['dateRecorded', 'duration', 'timeZone', 'vmid', 'callerName', 'callerNumber', 'mediaSize', ]


def get_user_cfg(username):
    user_cfg = cfg.site['Users'][username]
    oauth_url = cfg.site["OauthURL"] + "/login"
    login_name = user_cfg['UserId'] + '@' + user_cfg['DomainName']
    password = user_cfg['AccountPassword']
    return login_name, password


@Trace(log)
def get_vm_metadata(username, category, fields=default_fields):
    retries = 2
    while True:
        try:
            microservices = Microservices(*get_user_cfg(username))
            break
        except ValueError:
            if retries > 0:
                log.warn("ValueError instantiating Microservices - retrying")
                retries -= 1
            else:
                raise
    category = category.lower()
    mds = microservices.get_vm_metadata(category.lower()).json()
    return [{field: str(md[field]) for field in fields} for md in mds]


@Trace(log)
def get_vmids(username, category):
    mds = get_vm_metadata(username, category)
    return [md['vmid'] for md in mds]



@Trace(log)
def get_age_minutes(timestamp):
    # timestamp is in format of vm metadata "dateRecorded" field: 'YYYY-MM-DD hh:mm:ss'
    utcnow = datetime.datetime.utcnow()
    timestamp_dt = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    delta = utcnow - timestamp_dt
    return delta.days * 24 * 60 + delta.seconds / 60


