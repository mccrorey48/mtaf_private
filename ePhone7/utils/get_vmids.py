import sys
sys.path = sys.path[1:]
from lib.wrappers import Trace
import lib.logging_esi as logging
from lib.user_exception import UserException as Ux
import requests
from ePhone7.config.configure import cfg
from time import time, sleep

log = logging.get_logger('esi.get_vmids')


@Trace(log)
def get_first_vmid_data(username, category):
    md = get_vm_metadata(category, username).json()[0]
    return {'name': md['callerName'], 'number': md['callerNumber'], 'duration': md['duration'], 'timestamp': md['dateRecorded']}


@Trace(log)
def get_vmids(username, category):
    rvvm = get_vm_metadata(category, username)
    for vm in rvvm.json():
        log.debug("get_vmids: %s vmid=%s" % (category, vm['vmid']))
        print vm['dateRecorded']
    return [vm['vmid'] for vm in rvvm.json()]


def get_vm_metadata(category, username):
    category = category.lower()
    if category not in ('new', 'saved', 'trash'):
        raise Ux('get_vmids category must be new, saved or trash: got %s' % category)
    user_cfg = cfg.site['Users'][username]
    roauth = requests.post(cfg.site["OauthURL"] + "/login", data=cfg.site["OauthUsername"] % (
        user_cfg['UserId'], user_cfg['DomainName'], user_cfg['AccountPassword']), headers=cfg.site["OauthHeaders"])
    access_token = roauth.json()["accessToken"]
    vvm_headers = {key: cfg.site["VVMHeaders"][key] for key in cfg.site["VVMHeaders"]}
    vvm_headers["Authorization"] = vvm_headers["Authorization"] % access_token
    sleep(2)
    rvvm = requests.get(cfg.site["VVMURL"] + "/" + category, headers=vvm_headers)
    log.debug("rvvm = %s" % rvvm)
    return rvvm


@Trace(log)
def vmid_count_incremented(username, category, old_vmid_count, timeout=60):
    start_time = time()
    while time() - start_time < timeout:
        new_vmid_count = len(get_vmids(username, category))
        increase = new_vmid_count - old_vmid_count
        if increase == 0:
            sleep(10)
            continue
        if increase == 1:
            return True
        if increase > 1:
            raise Ux("vmid count increased by %d" % increase)
    else:
        return False


if __name__ == "__main__":
    print get_first_vmid_data('R2d2User', 'new')
    # vmids = get_vmids('R2d2User', 'new')
    # for vmid in vmids:
    #     print vmid
