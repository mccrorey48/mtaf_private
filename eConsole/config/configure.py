import os
import json
from mtaf.user_exception import UserException as Ux
from six import print_


class Cfg:

    def __init__(self):
        self.site_name = os.getenv('MTAF_SITE', 'default')
        with open("eConsole/config/site.json") as f:
            self.all_site_cfgs = json.load(f)
        self.site = None

    def set_test_target(self, target):
        # - self.all_site_cfgs is the dictionary containing the output of the
        #   json.load() performed on eConsole/config/site.json
        # - site.json contains configuration data needed at runtime to perform
        #   tests on eConsole; the values needed will depend on the test target
        #   (i.e., which web app URL is being tested) and the site (which host machine
        #   is running the tests)
        if self.site_name in self.all_site_cfgs:
            # - site_cfg gets the  name/value pair from the self.all_site_cfgs dictionary
            #   that has the name equal to self.site_name
            # - the value of this pair is a dictionary
            # - this dictionary contains:
            #     - a name/value pair for each test target, currently "devdash" or "aws"
            #       (should change to "svlab", "staging", "production" to match accelQ
            #       regression test configuration and comply with usage by web dev team)
            #     - the value of each of the test-target-specific pairs is a dictionary
            #       containing data that depends on the test target selected, like user
            #       account information, app url, etc.
            #     - there is also a name/value pair called "common"; the value of thi pair
            #       is a dictionary containing data that is the same for all test targets
            site_cfg = self.all_site_cfgs[self.site_name]
            # - once the target-specific data has been assigned to "site_cfg", the site_cfg
            #   attribute "system" will have a value of "production" or "svlab"; this value
            #   is assigned to "system"
            system = site_cfg[target]['system']
            # - self.all_site_cfgs has a name/value pair with the name "defaults", which
            #   contains "production" and "svlab" attributes
            # - the value of the "production" or "svlab" attribute (depending on the value
            #   now assigned to "system") is used as the initial value of the self.site
            #   dictionary
            self.site = self.all_site_cfgs['defaults'][system]
            # - self.site is then updated with the "common" data, then with the target-specific
            #   data, so it will now contain all data needed by the MTAF at runtime for the
            #   specified test target, when running tests on the test host identified by
            #   "site_name"
            self.site.update(site_cfg['common'])
            self.site.update(site_cfg[target])
        else:
            raise Ux('site name %s not found in config file' % self.site_name)


cfg = Cfg()

if __name__ == '__main__':
    cfg.set_test_target('devdash')
    print_(json.dumps(cfg.site, sort_keys=True, indent=4, separators=(',', ': ')))
