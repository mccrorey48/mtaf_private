from mtaf import mtaf_logging
from eConsole.config.configure import cfg
from eConsole.views import *
from mtaf.user_exception import UserException as Ux
import datetime
from time import strftime, localtime
import os

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
    context.app_version = ''
    context.browser_log = []
    context.run_substep = run_substep(context)
    context.make_assertion = make_assertion(context)
    base_view.open_browser()


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
    base_view.get_url(cfg['portal_url'][context.config.userdata['portal_server']])
    if not login_view.element_is_present('LoginButton'):
        logged_in_view.logout()
    if not context.app_version:
        context.app_version = login_view.find_named_element("AppVersion").text.split('eConsole Version: ')[1]
        with open('app_version.txt', 'w') as f:
            f.write(context.app_version)


def after_scenario(context, scenario):
    global substeps
    if scenario.status == 'failed' and 'fake' not in str(context.config.tags).split(','):
        if 'critical' in scenario.tags + scenario.feature.tags:
            context._config.stop = True
        if scenario.status == 'failed':
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_path = base_view.get_screenshot_as_png('exception-%s' % timestamp, scale=0.5)
            substeps += 'screenshot = %s\n' % screenshot_path
    try:
        logged_in_view.logout()
    except Ux:
        log.info("got user exception attempting to log out")
        context._config.stop = True
    if scenario.steps[-1].exception:
        base_view.close_browser()
        with open('tmp/steps.txt', 'w') as f:
            f.write(substeps)
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
    log_items = base_view.get_driver().get_log('browser')
    for log_item in log_items:
        log_item['step'] = step.name
        log_item['scenario'] = context.scenario.name
        log_item['feature'] = context.feature.name
        context.browser_log.append(log_item)


def after_all(context):
    global substeps
    base_view.close_browser()
    logdir = os.getenv('MTAF_LOG_DIR', 'log')
    timestamp = strftime('%m_%d_%y-%H_%M_%S', localtime())
    browser_fname = os.path.join(logdir, 'browser_%s.log' % timestamp)
    with open(browser_fname, 'w') as f:
        for log in context.browser_log:
            if len(log['message']):
                timestamp = strftime('%m/%d/%y %H:%M:%S', localtime(log['timestamp'] / 1000))
                f.write('timestamp: %s\nfeature: %s\nscenario: %s\nstep: %s\nmessage: ' % (
                    timestamp, log['feature'], log['scenario'], log['step']))
                f.write(log['message'].encode('utf-8') + '\n\n')
    substeps += 'browser_log = %s\n' % browser_fname
    with open('tmp/steps.txt', 'w') as f:
        f.write(substeps)

