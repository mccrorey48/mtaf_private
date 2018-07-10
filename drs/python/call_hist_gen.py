from mtaf.simple_pj import SoftphoneManager
from time import sleep, time
import os
from six import print_
import csv

# reads a csv file for multiple user account uri and passwords
# (the csv file is exported by the nms from the "devices" page)
# then registers up to max_user_count phones concurrently;
# after a sleep, unregisters the phones and exits
#
# this script uses mtaf libraries to create softphones; it must be run
# from the top level "mtaf" directory in the new_arch branch of the
# mtaf repo (clone from https://bitbucket.org/estech/mtaf)
#
# the recommended way to set up the mtaf as a runtime environment
# is:
#
# - start with a clean Python virtualenv
# - clone the mtaf repo
# - check out the new_arch branch
# - cd to mtaf/packages/mtaf
# - enter ". develop" to make the mtaf package accessible for imports
# - build the pjsip python API (see MTAF confluence pages for help) and
#   install into the virtualenv so softphones can be instantiated

softphone_manager = SoftphoneManager()


def get_softphone(uri, password):
    proxy = 'nr5.cpbx.esihs.net'
    null_snd = True
    dns_list = ['10.0.50.156']
    tcp = False
    reg_wait = False
    return softphone_manager.get_softphone(uri, proxy, password, null_snd, dns_list, tcp, reg_wait)


passwords={}
with open(os.path.join('drs', 'python', 'test2_tigerteam_users.csv')) as f:
    reader = csv.DictReader(f, quotechar="'")
    for row in reader:
        uri = row['aor']
        if uri.split('@')[0][-1] != 'a':
            passwords[uri] = row['authentication_key']
uris = sorted(passwords.keys())
max_user_count = 2
softphone_pairs = []
for index in range(0, max_user_count, 2):
    if index > len(uris):
        break
    caller_uri = uris[index]
    called_uri = uris[(index + 1) % len(uris)]
    print_("%s --> %s" % (caller_uri, called_uri))
    caller = get_softphone(caller_uri, passwords[caller_uri])
    called = get_softphone(called_uri, passwords[called_uri])
    softphone_pairs.append({"caller": caller, "called": called})
sleep(2)
for i in range(1000):
    for pair in softphone_pairs:
        pair["called"].set_incoming_response(200)
        pair["caller"].make_call(pair["called"].uri)
        sleep(5)
        # # for pair in softphone_pairs:
        print_("caller %s call time: %s" % (pair["caller"].account_info.uri,
                                            time() - pair["caller"].account_info.call_start_time))
        print_("called %s call time: %s" % (pair["called"].account_info.uri,
                                            time() - pair["called"].account_info.call_start_time))
        pair["caller"].end_call()
        pair["called"].wait_for_call_status('idle', 15)
for pair in softphone_pairs:
    pair["caller"].unregister()
    pair["called"].unregister()
