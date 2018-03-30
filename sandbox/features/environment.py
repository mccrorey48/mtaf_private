# from os import path, makedirs
from time import sleep
from mtaf import mtaf_logging
# from ePhone7.config.configure import cfg
# from ePhone7.views import base_view
# from ePhone7.utils.get_softphone import softphone_manager

log = mtaf_logging.get_logger('mtaf.environment')
substeps=''


def run_substep(context):
    def wrapped(step_name):
        context._is_substep = True
        context.execute_steps(unicode('Then ' + step_name))
    return wrapped

def before_all(context):
    global substeps
    substeps=''
    context._is_substep = False
    context.run_substep = run_substep(context)


def before_feature(context, feature):
    mtaf_logging.push_msg_src('feature')
    log.info('feature.name: %s' % feature.name)


def after_feature(context, feature):
    mtaf_logging.pop_msg_src()


def before_scenario(context, scenario):
    mtaf_logging.push_msg_src('  scenario')
    log.info('scenario.name: %s' % scenario.name)


def after_scenario(context, scenario):
    # softphone_manager.end_all_calls()
    # tags = str(context._config.tags).split(',')
    # if 'fake' not in tags and 'json' not in tags:
    #     base_view.close_appium()
    #     base_view.open_appium()
    #     base_view.startup()
    if scenario.status == 'failed' and 'critical' in scenario.tags + scenario.feature.tags:
        context._config.stop = True
        sleep(1)
    mtaf_logging.pop_msg_src()


def before_step(context, step):
    global substeps
    if context._is_substep:
        if substeps[-1] != '\n':
            substeps += ',passed,0.000\n'
        substeps += "substep = %s" % step.name
    else:
        substeps += "step = %s\n" % step.name
    mtaf_logging.push_msg_src('    step: %s' % step.name[:30])
    log.info('step.name: %s' % step.name)


def after_step(context, step):
    global substeps
    if context._is_substep:
        substeps += (',%s,%.3f\n' % (step.status.name, step.duration))
        context._is_substep = False
    if step.exception:
        log.info("EXCEPTION in step %s" % step.name)
#     if 'fake' not in str(context._config.tags).split(','):
#         if step.status == 'failed':
#             xml = base_view.get_source()
#             try:
#                 makedirs(cfg.xml_folder)
#             except OSError as e:
#                 # ignore 'File exists' error but re-raise any others
#                 if e.errno != 17:
#                     raise e
#             xml_fullpath = path.join(cfg.xml_folder, 'exception.xml')
#             log.info("saving xml %s" % xml_fullpath)
#             with open(xml_fullpath, 'w') as _f:
#                 _f.write(xml.encode('utf8'))
#             base_view.get_screenshot_as_png('exception', cfg.test_screenshot_folder)
    mtaf_logging.pop_msg_src()


def after_all(context):
    tags = str(context._config.tags).split(',')
#     if 'fake' not in tags and 'json' not in tags:
#         base_view.close_appium()
    with open('tmp/steps.txt', 'w') as f:
        f.write(substeps)

