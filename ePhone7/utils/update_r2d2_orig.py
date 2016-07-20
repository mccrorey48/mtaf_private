# from selenium.webdriver.firefox.webdriver import WebDriver
from appium import webdriver
# from selenium.webdriver.common.action_chains import ActionChains
# import time

success = True
desired_caps = {}
desired_caps['appium-version'] = '1.0'
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '4.4'
desired_caps['deviceName'] = 'r2d2'
desired_caps['appPackage'] = 'com.esi_estech.ditto'
desired_caps['appActivity'] = '.activities.MainViewActivity'

wd = webdriver.Remote('http://10.100.33.108:4723/wd/hub', desired_caps)
wd.implicitly_wait(60)


# # automatically generated, not used
# def is_alert_present(wd):
# 	try:
# 		wd.switch_to_alert().text
# 		return True
# 	except:
# 		return False

try:
    wd.find_element_by_name("Options").click()
    wd.find_element_by_xpath("//android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]/android.view.View[1]/android.widget.FrameLayout[2]/android.widget.RelativeLayout[1]/android.widget.ListView[1]/android.widget.LinearLayout[10]").click()
    wd.find_element_by_xpath("//android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]").click()
    wd.find_element_by_xpath("//android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.Button[1]").click()
    wd.find_element_by_xpath("//android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]/android.view.View[1]/android.widget.FrameLayout[2]/android.widget.RelativeLayout[1]/android.widget.ListView[1]/android.widget.LinearLayout[10]").click()
    wd.find_element_by_xpath("//android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[2]").click()
    wd.find_element_by_xpath("//android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.RelativeLayout[1]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.Button[2]").click()
    wd.find_element_by_xpath("//android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.RelativeLayout[1]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.Button[2]").click()
finally:
    wd.quit()
    if not success:
        raise Exception("Test failed.")
