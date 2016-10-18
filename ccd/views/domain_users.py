import lib.logging_esi as logging
from ccd.utils.configure import cfg
import re
from ccd.views.domain import DomainView

log = logging.get_logger('esi.domain_music_on_hold_view')


class DomainUsersView(DomainView):

    locators = {
        "TrashCanIconSub": {"by": "xpath", "value": "td[5]/a"},
        "ConfirmYes": {"by": "xpath", "value": "/html/body/div[2]/div[2]/div/a[1]"}
    }

    def __init__(self):
        super(DomainUsersView, self).__init__()
        self.view_name = "domain_music_on_hold"
        self.page_title = "Manager Portal - Users"

    def find_deletable_user_rows(self):
        accounts = [cfg.site["Accounts"][key] for key in cfg.site["Accounts"] if cfg.site["Accounts"][key]["delete"] == "true"]
        account_names = ["%s %s" % (account['name1'], account['name2']) for account in accounts]
        rows = self.find_table_rows_by_text(1, cfg.site['TestUserPartialName'], partial=True)
        data_locator = self.get_locator("RowDataSub")
        data_locator["value"] = re.sub("column", "%s" % 1, data_locator["value"])
        for row in rows[:]:
            text = self.find_sub_element_by_locator(row, data_locator).text
            if text not in account_names:
                rows.remove(row)
        return rows


domain_users_view = DomainUsersView()
