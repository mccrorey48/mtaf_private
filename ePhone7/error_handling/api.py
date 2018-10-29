import requests
from time import time
from mtaf import mtaf_logging
from mtaf.decorators import Trace


log = mtaf_logging.get_logger('mtaf.api')
user = '1000'
password = '1000'
domain = 'svauto-js'
mac = '00304d02b475'
model = 'ESI ePhone7'
url = 'http://nms-s3.sv.epo01.esihs.net/ns-api/'
client_id = 'omp@nms-s3.sv.epo01.esihs.net'
client_secret = 'd51a3b633fb5a64db9513d76a58ffce8'

# __all__ = ['api', 'user']


class Api(object):
    log = mtaf_logging.get_logger('mtaf.api')
    user = '1000'
    password = '1000'
    domain = 'svauto-js'
    mac = '00304d02b475'
    model = 'ESI ePhone7'
    url = 'http://nms-s3.sv.epo01.esihs.net/ns-api/'
    client_id = 'omp@nms-s3.sv.epo01.esihs.net'
    client_secret = 'd51a3b633fb5a64db9513d76a58ffce8'

    def __init__(self):
        oauth_url = url + 'oauth2/token/'
        data = {'grant_type': 'password',
                'client_id': '%s' % client_id,
                'client_secret': '%s' % client_secret,
                'username': '%s' % user + '@' + '%s' % domain + '.com',
                'password': '%s' % password}
        req = requests.post(oauth_url, data)
        if req.status_code == 200:
            self.oauth_tokens = req.json()
            print "POST get oauth %s data=%s status_code=%s" % (url, data, req.status_code)
            log.debug("POST get oauth %s data=%s [status code=%s]" % (url, data, req.status_code))
            log.debug("got oauth tokens: %s" % self.oauth_tokens)
        else:
            log.debug("Not able to request Access Token, got %s" % req.status_code)

    @Trace(log)
    def refresh(self):
        url_refresh = url + 'oauth2/token/' + 'refresh'
        data = {'grant_type': 'refresh_token',
                'client_id': '%s' % client_id,
                'client_secret': '%s' % client_secret,
                'refresh_token': self.oauth_tokens['refresh_token']}
        headers = {'Authorization': 'Bearer %s' % self.oauth_tokens['access_token'],
                   'Accept': 'application/json'}
        req = requests.post(url_refresh, data, headers)
        if req.status_code == 200:
            self.oauth_tokens = req.json()
            log.debug("refresh oauth tokens: %s" % self.oauth_tokens)
        else:
            log.info("Not able to request Refresh Token, got %s" % req.status_code)

    @Trace(log)
    def oauth_age_check(self):
        ttx = self.oauth_tokens['expires_in'] + time()
        log.debug("time to expiration: %.1f" % ttx)
        if time() > ttx:
            log.debug("current time %s pass expiration %s time" % (time(), ttx))
            self.refresh()

    @Trace(log)
    def get_device_data(self):
        self.oauth_age_check()
        data = {'object': 'device',
                'action': 'read',
                'domain': '%s' % domain,
                'device': 'sip:%s' % user + '@' + '%s' % domain}
        headers = {'Authorization': 'Bearer %s' % self.oauth_tokens['access_token'],
                   'Accept': 'application/json'}
        req = requests.post(url, data=data, headers=headers)
        response = req.json
        while response['device']:
            if req.json['device'] == 'sip:%s' % user + '@' + '%s' % domain:
                log.debug("POST get device %s data=%s [status code=%s]" % (url, data, req.status_code))
                return True
            else:
                log.info("Not able to request Device Info, got %s" % req.status_code)
                return False
        else:
            log.debug('device does not exist')
            return False

    @Trace(log)
    def delete_device(self):
        self.oauth_age_check()
        data = {'object': 'device',
                'action': 'delete',
                'device': 'sip:%s' % user + '@' + '%s' % domain}
        headers = {'Authorization': 'Bearer %s' % self.oauth_tokens['access_token'],
                   'Accept': 'application/json'}
        device_info = self.get_device_data()
        if not device_info:
            log.debug("device does not exist")
        else:
            req = requests.post(url, data=data, headers=headers)
            if req.status_code == 200:
                log.debug("POST delete device %s data=%s [status code=%s]" % (url, data, req.status_code))
                log.debug("device was deleted")
                return True
            else:
                log.info("Not able to Delete Device, got %s" % req.status_code)
                return False

    @Trace(log)
    def create_device(self):
        self.oauth_age_check()
        data = {'object': 'device',
                'action': 'create',
                'domain': '%s' % domain,
                'device': 'sip:%s' % user + '@' + '%s' % domain,
                'user': '%s' % user,
                'mac': '%s' % mac,
                'model': '%s' % model}
        headers = {'Authorization': 'Bearer %s' % self.oauth_tokens['access_token'],
                   'Accept': 'application/json'}
        device_info = self.get_device_data()
        if device_info:
            log.debug("Device does exist")
        else:
            req = requests.post(url, data=data, headers=headers)
            print "POST create device %s data=%s headers=%s status_code=%s" % (url, data, headers, req.status_code)
            if req.status_code == 200:
                log.debug("POST create device %s data=%s [status code=%s]" % (url, data, req.status_code))
                log.debug("Device was created")
                return True
            else:
                log.info("Not able to Create Device, got %s" % req.status_code)
                return False


api = Api()

