# This will read a Registrar_tac csv file (as downloaded from the svlab nms devices page for domain SVAutoDRS)
# which should be saved as "mtaf/ePhone7/config/reg.csv"
#
# It will then update "mtaf/ePhone7/config/cfg_site.json" to contain corresponding passwords for user entries where
# the entry type is "drs_test_user"
#
# Then dbutils.py can be used to update the configuration on the vqda1 or localhost mongodb configuration database
# so that the new configurations can be picked up by "mtaf/ePhone7/configure.py" for running DRS and load tests
#
import json
import csv
import os
import six

cfg_dir = os.path.join('ePhone7', 'config')
with open(os.path.join(cfg_dir, 'e7_site.json')) as f:
    sites = json.loads(f.read())

new_pws = {}

with open(os.path.join(cfg_dir, 'reg.csv')) as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['aor'] == "sip:%s@%s" % (row['subscriber_name'], row['authentication_realm']):
            new_pws[row['subscriber_name']] = row['authentication_key']

site = sites['mm_svlab']
for d in site:
    if d['type'] == 'drs_test_user':
        d['PhonePassword'] = new_pws[d['UserId']]

for d in sites['mm_svlab']:
    if d['type'] == 'drs_test_user':
        six.print_(d['UserId'], d['PhonePassword'], new_pws[d['UserId']])

with open(os.path.join(cfg_dir, 'e7_site.json'), 'w') as f:
    f.write(json.dumps(sites, sort_keys=True, indent=4, separators=(',', ': ')))
