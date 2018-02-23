import os
import json
from lib.user_exception import UserException as Ux


class Cfg:

    def __init__(self):
        self.site_name = os.getenv('MTAF_SITE', 'default')
        with open("eConsole/config/site.json") as f:
            self.all_site_cfgs = json.load(f)
        self.site = None

    def set_test_target(self, target):
        if self.site_name in self.all_site_cfgs:
            site_cfg = self.all_site_cfgs[self.site_name]
            system = site_cfg[target]['system']
            self.site = self.all_site_cfgs['defaults'][system]
            self.site.update(site_cfg['common'])
            self.site.update(site_cfg[target])
        else:
            raise Ux('site name %s not found in config file' % self.site_name)


cfg = Cfg()

if __name__ == '__main__':
    cfg.set_test_target('devdash')
    print json.dumps(cfg.site, sort_keys=True, indent=4, separators=(',', ': '))
