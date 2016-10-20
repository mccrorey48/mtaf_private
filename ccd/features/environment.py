from ccd.utils.configure import cfg
from ccd.views import base_view


def before_all(context):
    ccd_server = context.config.userdata.get('ccd_server')
    if 'cfg_server' in context.config.userdata:
        cfg_server = context.config.userdata.get('cfg_server')
    else:
        cfg_server = 'vqda'
    cfg.set_site(cfg_server, ccd_server)
    base_view.open_browser()


def after_scenario(context, scenario):
    pass

# @capture
def after_all(context):
    base_view.close_browser()
