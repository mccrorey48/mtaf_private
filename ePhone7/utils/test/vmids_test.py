from ePhone7.utils.vvm_microservice import *

mds = get_vm_metadata('R2d2User', 'new', fields={'duration', 'dateRecorded', 'callerName', 'callerNumber'})

for md in mds[:8]:
    print "%-14s%-18s     %s sec" % (md['callerNumber'], md['dateRecorded'], md['duration'])
