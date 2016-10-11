import lib.common.logging_esi as logging
from lib.common.wrappers import Trace
from ccd.views.reseller import ResellerView
from ccd.utils.configure import cfg
from lib.common.user_exception import UserException as Ux
from time import sleep

log = logging.get_logger('esi.reseller_domains_view')


class ResellerDomainsView(ResellerView):

    def __init__(self):
        super(ResellerDomainsView, self).__init__()
        self.view_name = "reseller domains"
        self.page_title = "Manager Portal - Domains"

    @Trace(log)
    def goto_test_domain_select(self):
        elems = self.find_elements_by_key("DomainName")
        # print "number of elements: %s" % len(elems)
        for elem in elems:
            # print "elem text = %s" % elem.text
            if elem.text == cfg.site["TestDomain"]:
                self.click_element(elem)
                break
        else:
            raise Ux("Domain %s not found in table" % cfg.site["TestDomain"])

    @Trace(log)
    def goto_test_domain_filter(self):
        self.filter_dropdown_and_click_result_by_link_text("DomainFilter", cfg.site["TestDomainMin"],
                                                           cfg.site["TestDomainExtended"])

    @Trace(log)
    def click_first_domain(self):
        elems = self.find_elements_by_key("DomainNames")
        if len(elems) > 0:
            self.click_element(elems[0])

    @Trace(log)
    def get_visible_domain_name_elems(self):
        return self.find_elements_by_key("DomainNames")

    @Trace(log)
    def first_row_is_test_domain(self):
        elems = self.find_elements_by_key("DomainNames")
        if len(elems) > 0:
            return elems[0].text == cfg.site['TestDomain']
        else:
            return False

    @Trace(log)
    def only_test_domain_is_in_table(self):
        elems = self.find_elements_by_key("DomainNames")
        log.debug("number of elems is %s" % len(elems))
        if len(elems) != 1:
            raise Ux("expected one domain to be in table, found %s" % len(elems))
        if elems[0].text != cfg.site['TestDomain']:
            raise Ux("expected domain in table to be %s, got %s" % (
                cfg.site['TestDomain'], elems[0].text))

reseller_domains_view = ResellerDomainsView()
