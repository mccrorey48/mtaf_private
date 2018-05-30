from mtaf import mtaf_logging
from eConsole.config.configure import cfg
from eConsole.views import *
from mtaf.user_exception import UserException as Ux
import datetime
from behave.log_capture import capture

log = mtaf_logging.get_logger('mtaf.environment')
behave_log = mtaf_logging.get_logger('behave')
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
    # base_view.open_browser()


def before_feature(context, feature):
    global substeps
    substeps += "feature = %s\n" % feature.name
    mtaf_logging.push_msg_src('feature')
    log.info('feature.name: %s' % feature.name)
    if 'skip' in feature.tags:
        feature.skip('Marked with @skip')
    else:
        behave_log.warn('Feature: %s' % feature.name)


def after_feature(context, feature):
    mtaf_logging.pop_msg_src()


def before_scenario(context, scenario):
    global substeps
    substeps += "scenario = %s\n" % scenario.name
    mtaf_logging.push_msg_src('  scenario')
    log.info('scenario.name: %s' % scenario.name)
    if 'skip' in scenario.effective_tags:
        scenario.skip('Marked with @skip')
    else:
        behave_log.warn('Scenario: %s' % scenario.name)


def after_scenario(context, scenario):
    global substeps
    if scenario.status == 'failed' and 'fake' not in str(context.config.tags).split(','):
        if 'critical' in scenario.tags + scenario.feature.tags:
            context._config.stop = True
        # if scenario.status == 'failed':
        #     timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        #     screenshot_path = base_view.get_screenshot_as_png('exception-%s' % timestamp, scale=0.2)
        #     substeps += 'screenshot = %s\n' % screenshot_path
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
    behave_log.warn('Step: %s' % step.name)


def after_step(context, step):
    global substeps
    if context.is_substep:
        substeps += (',%s,%.3f\n' % (step.status.name, step.duration))
        context.is_substep = False
    if step.exception:
        log.info("EXCEPTION in step %s" % step.name)
        context._config.stop = True
    mtaf_logging.pop_msg_src()


def after_all(context):
    tags = str(context.config.tags).split(',')
    # if 'fake' not in tags and 'json' not in tags:
    #     base_view.close_appium()
    with open('tmp/steps.txt', 'w') as f:
        f.write(substeps)

