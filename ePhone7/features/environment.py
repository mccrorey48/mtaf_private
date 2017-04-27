from ePhone7.utils.configure import cfg
from ePhone7.views import base_view
import lib.logging_esi as logging
from os import path, makedirs
log = logging.get_logger('esi.environment')


def before_all(context):
    site_tag = context.config.userdata.get('site_tag')
    if 'cfg_server' in context.config.userdata:
        cfg_server = context.config.userdata.get('cfg_server')
    else:
        cfg_server = 'vqda1'
    cfg.set_site(cfg_server, site_tag)
    if 'fake' not in str(context._config.tags).split(','):
        # base_view.open_appium()
        base_view.open_appium('nolaunch', force=True, timeout=60)
        base_view.startup()


def before_feature(context, feature):
    logging.push_msg_src('feature')
    log.info('feature.name: %s' % feature.name)


def after_feature(context, feature):
    logging.pop_msg_src()


def before_scenario(context, scenario):
    logging.push_msg_src('  scenario')
    log.info('scenario.name: %s' % scenario.name)


def after_scenario(context, scenario):
    logging.pop_msg_src()


def before_step(context, step):
    logging.push_msg_src('    step: %s' % step.name[:30])
    log.info('step.name: %s' % step.name)


def after_step(context, step):
    if 'fake' not in str(context._config.tags).split(','):
        if step.status == 'failed':
            xml = base_view.get_source()
            try:
                makedirs(cfg.xml_folder)
            except OSError as e:
                # ignore 'File exists' error but re-raise any others
                if e.errno != 17:
                    raise e
            xml_fullpath = path.join(cfg.xml_folder, 'exception.xml')
            log.info("saving xml %s" % xml_fullpath)
            with open(xml_fullpath, 'w') as _f:
                _f.write(xml.encode('utf8'))
            base_view.get_screenshot_as_png('exception', cfg.test_screenshot_folder)
        # elif step.name == 'The reboot alert window appears':
        #     # handle rebooting the ePhone7 before continuing
        #     base_view.close_appum()
    logging.pop_msg_src()


def after_all(context):
    base_view.close_appium()

