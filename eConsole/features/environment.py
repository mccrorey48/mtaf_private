import lib.logging_esi as logging
from eConsole.config.configure import cfg
from eConsole.views import *
from lib.user_exception import UserException as Ux
import datetime

logging.console_handler.setLevel(logging.INFO)
log = logging.get_logger('esi.environment')
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
    cfg.set_test_target(context.config.userdata.get('portal_server'))
    global substeps
    substeps = ''
    context.is_substep = False
    context.run_substep = run_substep(context)
    context.make_assertion = make_assertion(context)
    tags = str(context.config.tags).split(',')
    base_view.open_browser()


def before_feature(context, feature):
    global substeps
    substeps += "feature = %s\n" % feature.name
    logging.push_msg_src('feature')
    log.info('feature.name: %s' % feature.name)


def after_feature(context, feature):
    logging.pop_msg_src()


def before_scenario(context, scenario):
    global substeps
    context.scenario_name = scenario.name
    substeps += "scenario = %s\n" % scenario.name
    logging.push_msg_src('  scenario')
    log.info('scenario.name: %s' % scenario.name)


def after_scenario(context, scenario):
    global substeps
    if scenario.status == 'failed' and 'fake' not in str(context.config.tags).split(','):
        if 'critical' in scenario.tags + scenario.feature.tags:
            context._config.stop = True
        if scenario.status == 'failed':
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_path = base_view.get_screenshot_as_png('exception-%s' % timestamp, cfg.site['screenshot_folder'],
                                                              scale=0.5)
            substeps += 'screenshot = %s\n' % screenshot_path
    base_view.logout()
    if scenario.steps[-1].exception:
        base_view.close_browser()
        with open('tmp/steps.txt', 'w') as f:
            f.write(substeps)
    logging.pop_msg_src()


def before_step(context, step):
    global substeps
    if context.is_substep:
        if substeps[-1] != '\n':
            substeps += ',passed,0.000\n'
        substeps += "substep = %s" % step.name
    else:
        substeps += "step = %s\n" % step.name
    logging.push_msg_src('    step: %s' % step.name[:40])
    log.info('step.name: %s' % step.name)


def after_step(context, step):
    global substeps
    if context.is_substep:
        substeps += (',%s,%.3f\n' % (step.status, step.duration))
        context.is_substep = False
    if step.exception:
        log.info("EXCEPTION in step %s" % step.name)
        context._config.stop = True
    logging.pop_msg_src()


def after_all(context):
    base_view.close_browser()
    with open('tmp/steps.txt', 'w') as f:
        f.write(substeps)

