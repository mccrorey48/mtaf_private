from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

import lib.common.logging_esi as logging_esi

logging_esi.console_handler.setLevel(logging_esi.INFO)
log = logging_esi.get_logger('esi.ccd_cron')
with logging_esi.msg_src_cm('importing modules'):
    import unittest
    from lib.chrome.actions import Actions
    from ccd.views.login import login_view

run_list = [
    'test_010_login_get_version'
    ]


class CronTests(unittest.TestCase):
    actions = Actions

    def test_010_login_get_version(self):
        login_view.login()


