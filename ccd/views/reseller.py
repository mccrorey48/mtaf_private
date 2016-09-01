import lib.common.logging_esi as logging
from lib.common.wrappers import Trace
from lib.common.user_exception import UserException as Ux
from ccd.views.base import BaseView
import re

log = logging.get_logger('esi.reseller_view')


class ResellerView(BaseView):
    @Trace(log)
    def __init__(self):
        super(ResellerView, self).__init__()
        self.version_info = None
        self.view_name = "reseller"

    @Trace(log)
    def goto_home(self):
        self.actions.click_element_by_key('HomeTab')

    @Trace(log)
    def goto_domains(self):
        self.actions.click_element_by_key('DomainsTab')

    @Trace(log)
    def goto_inventory(self):
        self.actions.click_element_by_key('InventoryTab')

    @Trace(log)
    def logout(self):
        self.actions.click_element_by_key("Logout")

    @Trace(log)
    def version_should_be_correct(self):
        source = self.actions.get_source()
        m = re.match('.*<!-- ESI Cloud Communication Dashboard (v\.\d+\.\d+\.\d+) build (\d+) Date: ([^-]*) -- (\S*)',
                 source, re.MULTILINE | re.DOTALL)
        if m:
            _version, _build, _date, _time = m.groups()
            log.debug("version info = %s", m.groups())
            _site = self.cfg.site
            self.actions.assertEqual(_version, _site['Version'], 'Expected version %s, actual %s' % (_version, _site['Version']))
            self.actions.assertEqual(_build, _site['Build'], 'Expected build %s, actual %s' % (_version, _site['Build']))
            self.actions.assertEqual(_date, _site['Date'], 'Expected date %s, actual %s' % (_version, _site['Date']))
            self.actions.assertEqual(_time, _site['Time'], 'Expected time %s, actual %s' % (_version, _site['Time']))
        else:
            raise Ux('failed to find version info')

reseller_view = ResellerView()
