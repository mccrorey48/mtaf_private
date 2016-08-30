import lib.common.logging_esi as logging
from ccd.utils.configure import cfg
from lib.chrome.actions import Actions
from lib.common.wrappers import Trace
from lib.common.user_exception import UserException as Ux
import re
from time import sleep

log = logging.get_logger('esi.login_view')


class ResellerHomeView:

    @Trace(log)
    def __init__(self):
        self.cfg = cfg
        self.actions = Actions(self)
        self.version_info = None

    @Trace(log)
    def version_should_be_correct(self):
        source = self.actions.driver.page_source
        m = re.match('.*<!-- ESI Cloud Communication Dashboard (v\.\d+\.\d+\.\d+) build (\d+) Date: ([^-]*) -- (\S*)',
                 source, re.MULTILINE | re.DOTALL)
        if m:
            _version, _build, _date, _time = m.groups()
            _site = self.cfg.site
            self.actions.assertEqual(_version, _site['Version'], 'Expected version %s, actual %s' % (_version, _site['Version']))
            self.actions.assertEqual(_build, _site['Build'], 'Expected build %s, actual %s' % (_version, _site['Build']))
            self.actions.assertEqual(_date, _site['Date'], 'Expected date %s, actual %s' % (_version, _site['Date']))
            self.actions.assertEqual(_time, _site['Time'], 'Expected time %s, actual %s' % (_version, _site['Time']))
        else:
            raise Ux('failed to find version info')

reseller_home_view = ResellerHomeView()
