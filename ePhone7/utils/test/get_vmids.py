import six
from ePhone7.utils.e7_microservices import get_e7_microservices

e7_microservices = get_e7_microservices('R2d2User')
vm_metadata = {
    'new': e7_microservices.get_vm_metadata('new'),
    'saved': e7_microservices.get_vm_metadata('saved'),
    'deleted': e7_microservices.get_vm_metadata('deleted')
}
for type in "new", "saved", "deleted":
    for vm in vm_metadata[type]:
        six.print_("%s: %s" % (type, vm['dateRecorded']))
        for key in vm:
            six.print_("   %15s: %s" % (key, vm[key]))
