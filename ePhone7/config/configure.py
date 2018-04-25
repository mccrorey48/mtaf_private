import os
import json
from mtaf.user_exception import UserException as Ux
from six import print_, iteritems


def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value)
                # for key, value in input.iteritems()}
                for key, value in iteritems(input)}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


class Site(object):
    _dict = {}

    def __getattr__(self, name):
        if name in self._dict:
            return self._dict[name]
        else:
            raise Ux('name "%s" not in site dictionary')

    def __getitem__(self, name):
        if name in self._dict:
            return self._dict[name]
        else:
            raise Ux('name "%s" not in site dictionary')

    def update(self, d):
        self._dict.update(d)


class Cfg(object):

    def __init__(self):
        self.site = Site()
        self.site_tag = os.getenv('MTAF_SITE')
        if self.site_tag is None:
            raise Ux('MTAF_SITE must be defined in the run-time environment')
        with open("ePhone7/config/site.json") as f:
            self.all_site_cfgs = json.load(f)
        # - self.all_site_cfgs is the dictionary containing the output of the
        #   json.load() performed on ePhone7/config/site.json
        # - site.json contains configuration data needed at runtime to perform
        #   tests on ePhone7; the values needed will depend on the site (which host
        #   machine is running the tests)
        # - self.all_site_cfgs will contain 3 name/value pairs. The names are:
        #        caps - value is a dictionary of named "desired capabilities" dictionaries;
        #               one of these is selected to be used when starting appium
        #        colors - value is a dictionary of colors used to compare with observed
        #                 colors of various elements displayed on the ePhone7 screen
        #        sites - named dictionaries of site-specific configuration information;
        #                the environment variable "MTAF_SITE" is used to determine
        #                which of these dictionaries will be saved in self.site
        #                (used in the test program as "cfg.site")
        #
        # first save the desired caps in "self.caps" and the colors in "self.colors"
        self.caps = byteify(self.all_site_cfgs["caps"])
        self.colors = byteify(self.all_site_cfgs["colors"])
        # next populate self.site with default values; self.site will then be updated with
        # site-specific values, which will override default values that have the same name
        # (self.site is a Site class instance, set up so that dictionary <name>/<value> pairs
        #
        self.site.update(byteify(self.all_site_cfgs['defaults']))
        if self.site_tag in self.all_site_cfgs["sites"]:
            self.site.update(byteify(self.all_site_cfgs["sites"][self.site_tag]))
        else:
            raise Ux('site name %s not found in config file' % self.site_tag)



cfg = Cfg()

if __name__ == '__main__':
    print_(cfg.site.XmlFolder)
    # print_(json.dumps(cfg.caps, sort_keys=True, indent=4, separators=(',', ': ')))
    # print_(json.dumps(cfg.colors, sort_keys=True, indent=4, separators=(',', ': ')))
    # print_(json.dumps(cfg.site, sort_keys=True, indent=4, separators=(',', ': ')))

