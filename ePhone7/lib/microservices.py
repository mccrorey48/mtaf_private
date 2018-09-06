from mtaf import mtaf_logging
from mtaf.decorators import Trace
from mtaf.user_exception import UserException as Ux

import requests
from time import time

log = mtaf_logging.get_logger('mtaf.microsvcs')

__all__ = ['get_microservices']
default_url = 'https://pro.esiapi.io/'
ms_dict = {}


@Trace(log)
def md_complete(md_array):
    for vm in md_array:
        for key in ['dateRecorded', 'callerName', 'vmid', 'mediaSize', 'duration', 'timeZone', 'callerNumber']:
            if key not in vm:
                return False
    return True


def get_microservices(login, password, url=default_url):
    if login not in ms_dict:
        max_tries = 2
        tries = 0
        while tries < max_tries:
            tries += 1
            try:
                ms_dict[login] = Microservices(login, password, url)
                break
            except ValueError:
                log.warn("ValueError instantiating Microservices - retrying")
        else:
            raise Ux('Microservices failed to start after %s tries' % tries)
    return ms_dict[login]


class Microservices(object):
    def __init__(self, username, password, url):
        self.oauth_url = url + 'aaa/v2/'
        self.vvm_url = url + 'vvm/v2/'
        path = self.oauth_url + 'login/'
        data = '{"username": "%s", "password": "%s"}' % (username, password)
        headers = {"Content-type": "application/json"}
        req = requests.post(path, data=data, headers=headers)
        self.oauth_tokens = req.json()
        log.debug("POST %s data=%s [%s]" % (path, data, req.status_code))
        log.debug("got oauth tokens: %s" % self.oauth_tokens)

    @Trace(log)
    def refresh(self):
        path = self.oauth_url + 'refresh'
        data = '{"refreshToken": "%s"}' % self.oauth_tokens['refreshToken']
        headers = {
            "Authorization": "Bearer %s" % str(self.oauth_tokens['accessToken']),
            "Content-Type": "application/json"
        }
        req = requests.post(path, data=data, headers=headers)
        print "POST %s data=%s headers=%s status_code=%s" % (path, data, headers, req.status_code)
        if req.status_code == 200:
            self.oauth_tokens = req.json()
            log.debug("got oauth tokens: %s" % self.oauth_tokens)

    def oauth_age_check(self):
        ttx = self.oauth_tokens['expires'] - time()
        log.debug("time to expiration: %.1f" % ttx)
        if ttx < 60:
            self.refresh()

    @Trace(log)
    def get_vm_metadata(self, category):
        self.oauth_age_check()
        if category not in ('new', 'saved', 'deleted'):
            raise Ux('get_vm_metadata category must be new, saved or deleted: got %s' % category)
        vvm_headers = {
            "Authorization": "Bearer %s" % self.oauth_tokens['accessToken'],
            "Content-Type": "application/json"
        }
        path = self.vvm_url + 'vm/metadata/' + category
        max_tries = 5
        tries = 5
        while tries > 0:
            tries -= 1
            req = requests.get(path, headers=vvm_headers)
            if req.status_code != 200:
                log.info("GET %s returned %s, %d retries left" % (path, req.status_code, tries))
                log.info(", %d retries left" % tries)
                continue
            try:
                md_array = req.json()
            except ValueError as e:
                log.info('GET %s got ValueError: "%s", %d retries left' % (path, e, tries))
                continue
            if md_complete(md_array):
                log.debug("VMID_DEBUG (%d %s vmids)" % (len(md_array), category))
                for md in md_array:
                    log.debug("VMID_DEBUG %s" % md['vmid'][3:23])
                return req.json()
            else:
                log.info("get_vm_metadata returned incomplete data, %d retries left" % tries)
        raise Ux('get_vm_metadata("%s") failed after %d tries' % (category, max_tries))

    @Trace(log)
    def get_vm_count(self, category):
        self.oauth_age_check()
        if category not in ('new', 'saved', 'deleted'):
            raise Ux('get_vm_count category must be new, saved or deleted: got %s' % category)
        vvm_headers = {
            "Authorization": "Bearer %s" % self.oauth_tokens['accessToken'],
            "Content-Type": "application/json"
        }
        path = self.vvm_url + 'vm/count/' + category
        req = requests.get(path, headers=vvm_headers)
        log.debug("GET %s [%s]" % (path, req.status_code))
        return req.json()['count']

    @Trace(log)
    def delete_one_vm(self, category, vmid):
        self.oauth_age_check()
        if category not in ('new', 'saved'):
            raise Ux('delete_one_vm category must be new or deleted: got %s' % category)
        vvm_headers = {
            "Authorization": "Bearer %s" % self.oauth_tokens['accessToken'],
            "Content-Type": "application/json"
        }
        path = self.vvm_url + 'vm/file/%s/%s' % (category, vmid)
        req = requests.delete(path, headers=vvm_headers)
        log.debug("DELETE %s [%s]" % (path, req.status_code))

    @Trace(log)
    def undelete_one_vm(self, vmid):
        self.oauth_age_check()
        vvm_headers = {
            "Authorization": "Bearer %s" % self.oauth_tokens['accessToken'],
            "Content-Type": "application/json"
        }
        data = '{"action": "restore"}'
        path = self.vvm_url + 'vm/file/deleted/%s' % vmid
        req = requests.post(path, headers=vvm_headers, data=data)
        log.debug("POST %s [%s]" % (path, req.status_code))

