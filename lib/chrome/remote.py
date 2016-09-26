from selenium import webdriver
from selenium.webdriver.common.by import By

from ccd.utils.configure import cfg
import lib.common.logging_esi as logging_esi
log = logging_esi.get_logger('esi.remote')


class Remote:
    def __init__(self):
        self.driver = None
        self.open()
        self.By = By

    def open(self):
        if self.driver is not None:
            log.debug('remote driver is already open')
        else:
            self.driver = webdriver.Chrome()
            # self.driver = webdriver.Remote(desired_capabilities=webdriver.DesiredCapabilities.CHROME,
            #                                command_executor=cfg.site["SeleniumUrl"])

    def close(self):
        if self.driver is None:
            log.debug('remote driver is already closed')
        else:
            self.driver.quit()
            self.driver = None

remote = Remote()
