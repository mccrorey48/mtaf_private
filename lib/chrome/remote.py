from selenium import webdriver


class Remote:
    def __init__(self):
        self.driver = webdriver.Remote(desired_capabilities=webdriver.DesiredCapabilities.CHROME,
                                       command_executor='http://localhost:4444/wd/hub')

remote = Remote()
