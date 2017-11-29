from lib.user_exception import UserException as Ux
from ePhone7.utils.e7_microservices import *
from time import sleep

e7_microservices = get_e7_microservices('R2d2User')
fwd_microservices = get_e7_microservices('Auto TesterC')
default_fields = ['dateRecorded', 'callerName', 'vmid', 'mediaSize', 'duration', 'timeZone', 'callerNumber']
vmids = {}


def get_all_metadata(msvc, max_per_category=5):
    for cat in 'new', 'saved', 'deleted':
        vmids[cat] = []
        mds = msvc.get_vm_metadata(cat)
        for md in mds[:max_per_category]:
            print "%7s: %s" % (cat, md)
            for field in default_fields:
                if field not in md:
                    raise Ux('field missing: %s' % field)
            vmids[cat].append(md['vmid'])


def refresh_test():
    print "tokens = %s" % e7_microservices.oauth_tokens
    for cat in 'new', 'saved', 'deleted':
        print "%s %s" % (cat, e7_microservices.get_vm_count(cat))
    sleep(2)
    e7_microservices.refresh()
    print "tokens = %s" % e7_microservices.oauth_tokens
    for cat in 'new', 'saved', 'deleted':
        print "%s %s" % (cat, e7_microservices.get_vm_count(cat))


# refresh_test()
# get_all_metadata(e7_microservices)
# print
# get_all_metadata(fwd_microservices)
print get_vmids('R2d2User', 'saved')
