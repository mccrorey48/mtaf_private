from ccd.utils.configure import cfg
from ccd.views import base_view


def before_all(context):
    server = context.config.userdata.get('server')
    cfg.set_site(server)
    base_view.open_browser()


def after_scenario(context, scenario):
    pass

# @capture
def after_all(context):
    base_view.close_browser()
