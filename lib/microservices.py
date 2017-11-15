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
        roauth = requests.post(self.oauth_url + 'login/', data='{"username": "%s", "password": "%s"}' % (username, password),
                               headers={"content-type": "application/json"})
        self.oauth_tokens = roauth.json()

    @Trace(log)
    def get_vm_metadata(self, category):
        if category not in ('new', 'saved', 'trash'):
            raise Ux('get_vmids category must be new, saved or trash: got %s' % category)
        vvm_headers = {
            "Authorization": "Bearer %s" % self.oauth_tokens['accessToken'],
            "Content-Type": "application/json"
        }
        sleep(3)
        path = self.vvm_url + 'vm/metadata/' + category
        rvvm = requests.get(path, headers=vvm_headers)
        log.debug("rvvm = %s" % rvvm)
        return rvvm

