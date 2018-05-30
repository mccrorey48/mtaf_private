import os
import json
from mtaf.user_exception import UserException as Ux
import six


class Cfg:

    def __init__(self):
        site_name = os.getenv('MTAF_SITE')
        if site_name is None:
            raise Ux("MTAF_SITE environment variable not set")
        cfg_filename = "eConsole/config/site.json"
        try:
            with open(cfg_filename) as f:
                all_site_cfgs = json.load(f)
        except IOError as e:
            raise Ux("%s" % e)
        if site_name not in all_site_cfgs:
            raise Ux('MTAF_SITE key "%s" not found in %s' % (site_name, cfg_filename))
        self.site = all_site_cfgs[site_name]

    def __getattr__(self, name):
        if name in self.site:
            return self.site[name]
        elif name == 'site':
            raise AttributeError('Cfg instance attribute "site" cannot be accessed directly' % name)
        else:
            raise AttributeError("Cfg instance has no attribute named %s" % name)

    def __getitem__(self, name):
        if name in self.site:
            return self.site[name]
        elif name == 'site':
            raise AttributeError('Cfg instance attribute "site" cannot be accessed directly' % name)
        else:
            raise AttributeError("Cfg instance has no attribute named %s" % name)


cfg = Cfg()

if __name__ == '__main__':
    six.print_(json.dumps(cfg.site, sort_keys=True, indent=4, separators=(',', ': ')))
