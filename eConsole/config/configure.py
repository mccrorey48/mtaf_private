import os
import json
from lib.user_exception import UserException as Ux


class Cfg:

    def __init__(self):
        self.site_name = os.getenv('MTAF_SITE', 'default')
        with open("eConsole/config/site.json") as f:
            self.site_cfgs = json.load(f)
        self.site = None

    def set_test_target(self, target):
        if self.site_name in self.site_cfgs:
            self.site = self.site_cfgs['defaults'][self.site_cfgs[self.site_name][target]['system']]
            target_cfg = self.site_cfgs[self.site_name][target]
            self.site.update(target_cfg)
        else:
            raise Ux('site name %s not found in config file' % self.site_name)


cfg = Cfg()

if __name__ == '__main__':
    cfg.set_test_target('devdash')
    print json.dumps(cfg.site, sort_keys=True, indent=4, separators=(',', ': '))
