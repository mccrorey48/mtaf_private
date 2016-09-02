import lib.common.logging_esi as logging
from lib.common.wrappers import Trace
from ccd.views.reseller import ResellerView
from ccd.utils.configure import cfg
from lib.common.user_exception import UserException as Ux
from time import sleep

log = logging.get_logger('esi.reseller_domains_view')


class ResellerDomainsView(ResellerView):

    @Trace(log)
    def __init__(self):
        super(ResellerDomainsView, self).__init__()
        self.version_info = None
        self.view_name = "reseller domains"
        self.page_title = "Manager Portal - Domains"

    @Trace(log)
    def goto_test_domain_select(self):
        elems = self.actions.find_elements_by_key("DomainName")
        # print "number of elements: %s" % len(elems)
        for elem in elems:
            # print "elem text = %s" % elem.text
            if elem.text == cfg.site["TestDomain"]:
                elem.click()
                break
        else:
            raise Ux("Domain %s not found in table" % cfg.site["TestDomain"])

        self.actions.find_element_by_key("DomainMessage")

    @Trace(log)
    def goto_test_domain_filter(self):
        elem = self.actions.find_element_by_key("DomainFilter")
        filter_text = cfg.site["TestDomainMin"]
        sleep(1)
        elem.send_keys(filter_text)
        sleep(1)
        self.actions.send_tab_to_element(elem)
        sleep(1)
        elems = self.actions.find_elements_by_key("DomainName")
        self.actions.assert_elements_count(elems, 1, "Filtered domain list")
        if elems[0].text != cfg.site["TestDomain"]:
            raise Ux("Incorrect domain %s selected, expected %s" % (elems[0].text, cfg.site["TestDomain"]))
        elems[0].click()
        self.actions.find_element_by_key("DomainMessage")

reseller_domains_view = ResellerDomainsView()
