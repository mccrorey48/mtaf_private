from time import time, sleep
import mtaf.mtaf_logging as logging
from mtaf.trace import Trace
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import Chrome, Firefox
from mtaf.user_exception import UserException as Ux
from mtaf.selenium_actions import SeleniumActions
import re
import os
from time import localtime, strftime

log = logging.get_logger('mtaf.angular_actions')


class AngularActions(SeleniumActions):

    cfg = None
    driver = None

    def __init__(self):
        super(AngularActions, self).__init__()
        self.ng_wrapper = '%(prefix)s' \
                          'var $inj;try{$inj=angular.element(document.querySelector(' \
                          '\'[data-ng-app],[ng-app],.ng-scope\')||document).injector()||' \
                          'angular.injector([\'ng\'])}catch(ex){' \
                          '$inj=angular.injector([\'ng\'])};$inj.get=$inj.get||$inj;' \
                          '$inj.get(\'$browser\').notifyWhenNoOutstandingRequests(%(handler)s)' \
                          '%(suffix)s'
        self.jquery_url = '//code.jquery.com/jquery-1.11.3.min.js'
        self.jquery_bootstrap = 'var a=document.getElementsByTagName(\'head\')[0];' \
                                'var b=document.createElement(\'script\');' \
                                'b.type=\'text/javascript\';b.src=document.location.' \
                                'protocol+\'%(jquery_url)s\';a.appendChild(b);'
        self.element_filter = lambda x: x.is_displayed()
        self.driver = None
        self.current_browser = None
        self.service_log_path = None
        self.webdriver_log_path = None

    def get_url(self, url):
        if self.driver is None:
            raise Ux('remote is not open')
        log.debug('getting url %s' % url)
        self.driver.get(url)

    def open_browser(self, browser='chrome'):
        if self.current_browser is not None:
            log.debug('browser is already open')
        else:
            mtaf_log_dir = os.getenv('MTAF_LOG_DIR', './log')
            if browser.lower() == 'chrome':
                self.service_log_path = os.path.join(mtaf_log_dir, 'service.log')
                self.webdriver_log_path = os.path.join(mtaf_log_dir, 'webdriver.log')
                self.driver = Chrome(service_log_path=self.service_log_path)
            elif browser.lower() == 'firefox':
                self.driver = Firefox()
            else:
                raise Ux('Unknown browser %s' % browser)
            self.driver.set_window_size(1280, 1024)
            self.current_browser = browser

    def close_browser(self):
        if self.current_browser is None:
            log.debug('browser is already closed')
        else:
            self.driver.quit()
            self.driver = None
            self.current_browser = None
            if self.service_log_path is not None and self.webdriver_log_path is not None:
                self.process_log(self.service_log_path, self.webdriver_log_path)

    @Trace(log)
    def process_log(self, srcpath="log/service.log", destpath="log/webdriver.log", verbose=False):
        re_time = re.compile('\[(\d+)\.(\d+)')
        with open(srcpath) as src:
            with open(destpath, 'w') as dest:
                lines = src.readlines()
                in_cmd = False
                in_resp = False
                last = False
                for line in lines:
                    line = line.rstrip()
                    if line.find('COMMAND') != -1:
                        in_cmd = True
                        first = True
                        if verbose:
                            print
                        dest.write('\n')
                    elif line.find('RESPONSE') != -1:
                        in_resp = True
                        first = True
                    else:
                        first = False
                    if first:
                        sec, ms = re_time.match(line).groups()
                        timestamp = strftime('%m/%d/%y %H:%M:%S', localtime(int(sec))) + '.' + ms
                        line = re_time.sub(timestamp, line)
                    if in_cmd or in_resp:
                        if len(line) > 0 and ((line[0] != ' ' and line[-1] != '{') or line[0] == '}'):
                            last = True
                        if verbose:
                            print line
                        dest.write(line + '\n')
                    if last:
                        in_cmd = False
                        in_resp = False
                        last = False

    @Trace(log)
    def wait_until_angular_ready(self, timeout=20):
        error = 'AngularJS is not ready in %d seconds' % timeout
        # we add more validation here to support transition
        # between AngularJs to non AngularJS page.
        script = self.ng_wrapper % {
            'prefix': 'var cb=arguments[arguments.length-1];if(window.angular){',
            'handler': 'function(){cb(true)}',
            'suffix': '}else{cb(true)}'
        }
        self.driver.set_script_timeout(timeout)
        try:
            WebDriverWait(self.driver, timeout).until(lambda driver: driver.execute_async_script(script), error)
        except TimeoutException:
            # prevent double wait
            pass
        except:
            # still inflight, second chance. let the browser take a deep breath...
            sleep(1)
            WebDriverWait(self.driver, timeout).until(lambda driver: driver.execute_async_script(script), error)

    @Trace(log)
    def wait_until_page_ready(self, *args, **kwargs):
        """Semi blocking API that incorporated different strategies for cross-browser support."""
        prefix = kwargs.pop('prefix', 'var cb=arguments[arguments.length-1];if(window.angular){')
        skip_stale_check = bool(kwargs.pop('skip_stale_check', False))
        if not skip_stale_check:
            jquery_bootstrap = self.jquery_bootstrap % {'jquery_url': self.jquery_url}
            prefix = 'if(!window.jQuery){%(jquery_bootstrap)s}%(prefix)s' % \
                     {'jquery_bootstrap': jquery_bootstrap, 'prefix': prefix}
        script = self.ng_wrapper % {'prefix': prefix,
                                    'handler': kwargs.pop('handler', 'function(){cb(true)}'),
                                    'suffix': '}else{cb(false)}'}
        timeout = 30
        sleep(0.5)
        if len(args) > 0 and not isinstance(args[0], WebElement):
            args = list(args)
            elems = self.find_named_elements(args[0])
            # require at least one to be found, but only pass the first one to the script
            if len(elems) == 0:
                raise Ux("No elements found with locator named %s" % args[0])
            args[0] = elems[0]
        if not skip_stale_check:
            WebDriverWait(None, timeout).until_not(EC.staleness_of(self.driver.find_element_by_tag_name('html')), '')
        self.driver.execute_async_script(script, *args)

    @Trace(log)
    def element_trigger_change(self):
        self.wait_until_page_ready()

