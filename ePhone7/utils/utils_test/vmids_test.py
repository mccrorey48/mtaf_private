from ePhone7.utils.get_vmids import get_vmids
from ePhone7.config.configure import cfg

vmids = get_vmids(cfg.site['DefaultForwardAccount'], 'new')

print "%d vmids found" % len(vmids)