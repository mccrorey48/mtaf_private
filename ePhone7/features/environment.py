from ePhone7.utils.configure import cfg
from ePhone7.views import base_view


def before_all(context):
    site_tag = context.config.userdata.get('site_tag')
    if 'cfg_server' in context.config.userdata:
        cfg_server = context.config.userdata.get('cfg_server')
    else:
        cfg_server = 'vqda'
    cfg.set_site(cfg_server, site_tag)
    base_view.open_appium()


def after_all(context):
    base_view.close_appium()
