from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

from time import sleep
import re

version_re = re.compile('.*<!-- ESI Cloud Communication Dashboard (v\.\d+\.\d+\.\d+) build (\d+) Date: ([^-]*) -- (\S*)', re.MULTILINE | re.DOTALL)
portal_url='http://alpha.esihs.net/portal/'
username = 'Jsabugo@tigerteam.esihs.net'
password = '1986'
# driver = webdriver.Chrome()
driver = webdriver.Remote(
    desired_capabilities=webdriver.DesiredCapabilities.FIREFOX,
    command_executor='http://localhost:4444/wd/hub')
driver.get(portal_url)
username_elem = driver.find_element_by_id('LoginUsername')
password_elem = driver.find_element_by_id('LoginPassword')
login_elem = driver.find_element_by_id('loginBtn')
action = ActionChains(driver)
action.move_to_element(username_elem).send_keys_to_element(username_elem, username)
action.move_to_element(password_elem).send_keys_to_element(password_elem, password)
action.move_to_element(login_elem).click(login_elem)
action.perform()
sleep(10)
source = driver.page_source
m = version_re.match(source)
if m:
    print 'version %s' % m.group(1)
    print 'build %s' % m.group(2)
    print 'date %s' % m.group(3)
    print 'time %s' % m.group(4)
driver.quit()

