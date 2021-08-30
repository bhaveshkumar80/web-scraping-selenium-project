from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time

opts = Options()
opts.add_argument("user-agent=whatever you want")
#opts.add_argument("start-maximized")
opts.add_argument('--ignore-certificate-errors')
opts.add_argument('--ignore-ssl-errors')

driver = webdriver.Chrome(chrome_options=opts, executable_path=r'G:\chromedriver.exe')

driver.get('https://www.immobilienscout24.de')

WebDriverWait(driver,20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,'//*[@id="gdpr-consent-notice"]')))
WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="save"]'))).click()

#actions = ActionChains(driver)
#actions.click(cookies)

search = driver.find_element_by_css_selector('#oss-location')
search.send_keys('Berlin')
#search.send_keys(Keys.RETURN)
time.sleep(10)
hit = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="oss-form"]/article/div/div[3]/button')))
hit.click()
time.sleep(5)
hit.click()