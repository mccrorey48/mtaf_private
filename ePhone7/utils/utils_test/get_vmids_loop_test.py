import sys
sys.path = sys.path[1:]
from lib.wrappers import Trace
import lib.logging_esi as logging
from lib.user_exception import UserException as Ux
import requests
from ePhone7.config.configure import cfg
from time import time, sleep

log = logging.get_logger('esi.get_vmids')


# @Trace(log)
def get_vmids(username, type):
    type = type.lower()
    if type not in ('new', 'saved', 'trash'):
        raise Ux('get_vmids type must be new, saved or trash: got %s' % type)
    user_cfg = cfg.site['Users'][username]
    while True:
        # roauth = requests.post(cfg.site["OauthURL"] + "/login", data=cfg.site["OauthUsername"] % (
        roauth = requests.post("https://pro.esiapi.io/aaa/v2/login", data=cfg.site["OauthUsername"] % (
            user_cfg['UserId'], user_cfg['DomainName'], user_cfg['AccountPassword']), headers=cfg.site["OauthHeaders"])
        print "roauth.status_code = %s" % roauth.status_code
        if roauth.status_code == 200:
            break
    # sleep(3)
    access_token = roauth.json()["accessToken"]
    vvm_headers = {key: cfg.site["VVMHeaders"][key] for key in cfg.site["VVMHeaders"]}
    vvm_headers["Authorization"] = vvm_headers["Authorization"] % access_token
    sleep(2)
    # rvvm = requests.get(cfg.site["VVMURL"] + "/new", headers=vvm_headers)
    while True:
        rvvm = requests.get("https://pro.esiapi.io/vvm/v2/vm/metadata/new", headers=vvm_headers)
        print "rvvm.status_code = %s" % rvvm.status_code
        if rvvm.status_code == 200:
            print
            break
    # # for vm in rvvm.json():
    # #     log.debug("get_vmids: %s vmid=%s" % (type, vm['vmid']))
    # # return [vm['vmid'] for vm in rvvm.json()]


@Trace(log)
def vmid_count_incremented(username, type, old_vmid_count, timeout=60):
    start_time = time()
    while time() - start_time < timeout:
        new_vmid_count = len(get_vmids(username, type))
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
    while True:
        vmids = get_vmids(cfg.site['DefaultForwardAccount'], 'new')
        # try:
        #     vmids = get_vmids(cfg.site['DefaultForwardAccount'], 'new')
        #     for vmid in vmids:
        #         print vmid
        # except ValueError:
        #     print "got ValueError"
