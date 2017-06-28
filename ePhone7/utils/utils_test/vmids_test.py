from ePhone7.views import voicemail_view
from ePhone7.config.configure import cfg

vmids = voicemail_view.get_vmids(cfg.site['DefaultForwardAccount'])

print "%d vmids found" % len(vmids)