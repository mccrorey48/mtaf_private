from mtaf import mtaf_logging
from mtaf.decorators import Trace

from ccd.utils.configure import cfg
from ccd.views.reseller import ResellerView
from lib.user_exception import UserException as Ux

log = mtaf_logging.get_logger('mtaf.reseller_domains_view')


class ResellerDomainsView(ResellerView):

    locators = {
        "DomainFilter": {"by": "id", "value": "domains"},
        "DomainName": {"by": "xpath", "value": "//tbody/tr/td[1]/a"},
        "DomainNames": {"by": "xpath", "value": "//tbody/tr/td/a"}
    }

    def __init__(self):
        super(ResellerDomainsView, self).__init__()
        self.view_name = "reseller domains"
        self.page_title = "Manager Portal - Domains"

    @Trace(log)
    def goto_test_domain_select(self):
        elems = self.find_named_elements("DomainName")
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
        elems = self.find_named_elements("DomainNames")
        if len(elems) > 0:
            self.click_element(elems[0])

    @Trace(log)
    def get_visible_domain_name_elems(self):
        return self.find_named_elements("DomainNames")

    @Trace(log)
    def first_row_is_test_domain(self):
        elems = self.find_named_elements("DomainNames")
        if len(elems) > 0:
            return elems[0].text == cfg.site['TestDomain']
        else:
            return False

    @Trace(log)
    def only_test_domain_is_in_table(self):
        elems = self.find_named_elements("DomainNames")
        log.debug("number of elems is %s" % len(elems))
        if len(elems) != 1:
            raise Ux("expected one domain to be in table, found %s" % len(elems))
        if elems[0].text != cfg.site['TestDomain']:
            raise Ux("expected domain in table to be %s, got %s" % (
                cfg.site['TestDomain'], elems[0].text))


reseller_domains_view = ResellerDomainsView()
