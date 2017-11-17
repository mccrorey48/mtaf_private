from lib.user_exception import UserException as Ux
from ePhone7.utils.vvm_microservice import *

vvm_microservice = VvmMicroservice('R2d2User')
default_fields = ['dateRecorded', 'callerName', 'vmid', 'mediaSize', 'duration', 'timeZone', 'callerNumber']
vmids = {}


def get_all_metadata(max_per_category=5, fields=default_fields):
    for cat in 'new', 'saved', 'deleted':
        vmids[cat] = []
        mds = vvm_microservice.get_vm_metadata(cat, fields)
        for md in mds[:max_per_category]:
            print "%s: %s" % (cat, md)
            for field in fields:
                if field not in md:
                    raise Ux('field missing: %s' % field)
            vmids[cat].append(md['vmid'])


for cat in 'new', 'saved', 'deleted':
    print "%s %s" % (cat, vvm_microservice.get_vm_count(cat)['count'])
get_all_metadata(5, ['vmid', 'duration', 'dateRecorded'])
# if len(vmids['deleted']) > 0:
#     vvm_microservice.undelete_one_vm(vmids['deleted'][0])
# for cat in 'new', 'saved', 'deleted':
#     print vvm_microservice.get_vm_count(cat)

# for vmid in vmids['new']:
#     vvm_microservice.delete_one_vm('new', vmid)
# for vmid in vmids['saved']:
#     vvm_microservice.delete_one_vm('saved', vmid)
#
# get_all_metadata(1000)
