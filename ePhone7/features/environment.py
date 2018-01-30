from mtaf import mtaf_logging
from ePhone7.config.configure import cfg
from ePhone7.views import base_view
from ePhone7.lib.utils.get_softphone import softphone_manager
from ePhone7.lib.utils.e7_microservices import get_e7_microservices
from mtaf.user_exception import UserException as Ux
import datetime

log = mtaf_logging.get_logger('mtaf.environment')
substeps = ''


def run_substep(context):
    def wrapped(step_name):
        context.is_substep = True
        if not context.execute_steps(unicode('Then ' + step_name)):
            raise Ux("run_substep: step '%s' not parseable" % step_name)
    return wrapped


def make_assertion(context):
    def wrapped(value_name, expected, actual):
        assert actual == expected, "Expected %s to be %s, got %s" % (value_name, expected, actual)
    return wrapped


def before_all(context):
    global substeps
    substeps = ''
    context.is_substep = False
    context.run_substep = run_substep(context)
    context.make_assertion = make_assertion(context)
    tags = str(context.config.tags).split(',')
    if 'fake' not in tags and 'json' not in tags:
        base_view.open_appium()
        base_view.wait_for_activity('.activities.MainViewActivity')


def before_feature(context, feature):
    global substeps
    substeps += "feature = %s\n" % feature.name
   mtaf_logging.push_msg_src('feature')
    log.info('feature.name: %s' % feature.name)


def after_feature(context, feature):
   mtaf_logging.pop_msg_src()


def before_scenario(context, scenario):
    global substeps
    substeps += "scenario = %s\n" % scenario.name
   mtaf_logging.push_msg_src('  scenario')
    log.info('scenario.name: %s' % scenario.name)
    if scenario.feature.name.lower().find('voicemail') != -1:
        e7_microservices = get_e7_microservices('R2d2User')
        context.existing_vm_metadata = {
            'new': e7_microservices.get_vm_metadata('new'),
            'saved': e7_microservices.get_vm_metadata('saved'),
            'deleted': e7_microservices.get_vm_metadata('deleted')
        }


def after_scenario(context, scenario):
    global substeps
    softphone_manager.end_all_calls()
    softphone_manager.set_defaults()
    tags = str(context.config.tags).split(',')
    # if 'fake' not in tags and 'json' not in tags:
    #     try:
    #         base_view.close_appium()
    #         base_view.open_appium()
    #         base_view.startup()
    #     except Ux as e:
    #         log.warn("after_scenario: got user exception %s" % e)
    if scenario.status == 'failed' and 'fake' not in str(context.config.tags).split(','):
        if 'critical' in scenario.tags + scenario.feature.tags:
            context._config.stop = True
        if scenario.status == 'failed':
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_path = base_view.get_screenshot_as_png('exception-%s' % timestamp, cfg.test_screenshot_folder,
                                                              scale=0.5)
            substeps += 'screenshot = %s\n' % screenshot_path
   mtaf_logging.pop_msg_src()


def before_step(context, step):
    global substeps
    if context.is_substep:
        if substeps[-1] != '\n':
            substeps += ',passed,0.000\n'
        substeps += "substep = %s" % step.name
    else:
        substeps += "step = %s\n" % step.name
   mtaf_logging.push_msg_src('    step: %s' % step.name[:40])
    log.info('step.name: %s' % step.name)


def after_step(context, step):
    global substeps
    if context.is_substep:
        substeps += (',%s,%.3f\n' % (step.status, step.duration))
        context.is_substep = False
    if step.exception:
        log.info("EXCEPTION in step %s" % step.name)
   mtaf_logging.pop_msg_src()


def after_all(context):
    tags = str(context.config.tags).split(',')
    if 'fake' not in tags and 'json' not in tags:
        base_view.close_appium()
    with open('tmp/steps.txt', 'w') as f:
        f.write(substeps)

