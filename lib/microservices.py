from lib.wrappers import Trace
import lib.logging_esi as logging
from lib.user_exception import UserException as Ux
import requests
from time import sleep

log = logging.get_logger('esi.microsvcs')


class Microservices(object):
    def __init__(self, username, password, url='https://pro.esiapi.io/'):
        self.oauth_url = url + 'aaa/v2/'
        self.vvm_url = url + 'vvm/v2/'
        path = self.oauth_url + 'login/'
        data = '{"username": "%s", "password": "%s"}' % (username, password)
        headers = {"content-type": "application/json"}
        req = requests.post(path, data=data, headers=headers)
        self.oauth_tokens = req.json()
        log.debug("POST %s data=%s [%s]" % (path, data, req.status_code))
        log.debug("got oauth tokens: %s" % self.oauth_tokens)

    @Trace(log)
    def get_vm_metadata(self, category):
        if category not in ('new', 'saved', 'deleted'):
            raise Ux('get_vmids category must be new, saved or deleted: got %s' % category)
        vvm_headers = {
            "Authorization": "Bearer %s" % self.oauth_tokens['accessToken'],
            "Content-Type": "application/json"
        }
        path = self.vvm_url + 'vm/metadata/' + category
        req = requests.get(path, headers=vvm_headers)
        log.debug("GET %s [%s]" % (path, req.status_code))
        return req

    @Trace(log)
    def get_vm_count(self, category):
        if category not in ('new', 'saved', 'deleted'):
            raise Ux('get_vm_count category must be new, saved or deleted: got %s' % category)
        vvm_headers = {
            "Authorization": "Bearer %s" % self.oauth_tokens['accessToken'],
            "Content-Type": "application/json"
        }
        path = self.vvm_url + 'vm/count/' + category
        req = requests.get(path, headers=vvm_headers)
        log.debug("GET %s [%s]" % (path, req.status_code))
        return req

    @Trace(log)
    def delete_one_vm(self, category, vmid):
        if category not in ('new', 'saved'):
            raise Ux('delete_one_vm category must be new or deleted: got %s' % category)
        vvm_headers = {
            "Authorization": "Bearer %s" % self.oauth_tokens['accessToken'],
            "Content-Type": "application/json"
        }
        path = self.vvm_url + 'vm/file/%s/%s' % (category, vmid)
        req = requests.delete(path, headers=vvm_headers)
        log.debug("DELETE %s [%s]" % (path, req.status_code))
        return req

    @Trace(log)
    def undelete_one_vm(self, vmid):
        vvm_headers = {
            "Authorization": "Bearer %s" % self.oauth_tokens['accessToken'],
            "Content-Type": "application/json"
        }
        data = '{"action": "restore"}'
        path = self.vvm_url + 'vm/file/deleted/%s' % vmid
        req = requests.post(path, headers=vvm_headers, data=data)
        log.debug("POST %s [%s]" % (path, req.status_code))
        return req

