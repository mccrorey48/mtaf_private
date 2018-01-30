from mtaf import mtaf_logging
from lib.user_exception import UserException as Ux
from selenium import webdriver
import os

log =mtaf_logging.get_logger('mtaf.environment')
substeps = ''


def run_substep(context):
    def wrapped(step_name):
        context.is_substep = True
        if not context.execute_steps(unicode('Then ' + step_name)):
            raise Ux("run_substep: step '%s' not parseable" % step_name)
    return wrapped


def before_all(context):
    global substeps
    substeps = ''
    context.is_substep = False
    context.run_substep = run_substep(context)
    tags = str(context.config.tags).split(',')


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
    if 'BROWSER' in context.config.userdata.keys():
        if context.config.userdata['BROWSER'] is None:
            browser = 'chrome'
        else:
            browser = context.config.userdata['browser']
    else:
        browser = 'chrome'
    # For some reason, python doesn't have switch case -
    # http://stackoverflow.com/questions/60208/replacements-for-switch-statement-in-python
    if browser == 'chrome':
        context.browser = webdriver.Chrome()
    elif browser == 'firefox':
        context.browser = webdriver.Firefox()
    elif browser == 'safari':
        context.browser = webdriver.Safari()
    elif browser == 'ie':
        context.browser = webdriver.Ie()
    elif browser == 'opera':
        context.browser = webdriver.Opera()
    elif browser == 'phantomjs':
        context.browser = webdriver.PhantomJS()
    else:
        raise Ux("browser you entered: " + browser + " is invalid value")

    context.browser.maximize_window()


def after_scenario(context, scenario):
    tags = str(context.config.tags).split(',')
    if scenario.status == 'failed':
        screenshot_dir = os.path.join('ppo', 'failed_scenarios_screenshots')
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        context.browser.save_screenshot(os.path.join(screenshot_dir, scenario.name + "_failed.png"))
        if 'critical' in scenario.tags + scenario.feature.tags:
            context._config.stop = True
   mtaf_logging.pop_msg_src()


def before_step(context, step):
    global substeps
    if context.is_substep:
        if substeps[-1] != '\n':
            substeps += ',passed,0.000\n'
        substeps += "substep = %s" % step.name
    else:
        substeps += "step = %s\n" % step.name
   mtaf_logging.push_msg_src('    step: %s' % step.name[:30])
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
    with open('tmp/steps.txt', 'w') as f:
        f.write(substeps)

