import json
import os


class Site(object):

    def __init__(self):
        with open(os.path.join('WebApp', 'config', 'site.json')) as f:
            self.dict = json.load(f)

    def __getitem__(self, item):
        if item in self.dict:
            return self.dict[item]
        else:
            return None

    def __getattr__(self, item):
        return self.__getitem__(item)


class Configure(object):
    def __init__(self):
        self.site = Site()


cfg = Configure()

if __name__ == '__main__':
    print cfg
