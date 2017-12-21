import json
import os

cfg = None
with open(os.path.join('AndroidApp', 'config', 'site.json')) as f:
    cfg = json.load(f)

if __name__ == '__main__':
    print cfg
