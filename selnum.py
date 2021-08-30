from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
import random

opts = Options()
opts.add_argument("user-agent=whatever you want")

opts.add_argument('--ignore-certificate-errors')
opts.add_argument('--ignore-ssl-errors')

driver = webdriver.Chrome(chrome_options=opts, executable_path=r'G:\chromedriver.exe')

driver.get('https://www.immobilienscout24.de/Suche/de/baden-wuerttemberg/anlageimmobilie')

def Captcha_Bypass(driver):

     other_place = WebDriverWait(driver, 15).until(
          EC.presence_of_element_located((By.CLASS_NAME, "main__part1"))
     )

     cl = random.choice(['geetest_dot', 'geetest_small', 'geetest_scan', 'geetest_ring'])
     print(cl)
     captcha = WebDriverWait(driver, 15).until(
          EC.presence_of_element_located((By.CLASS_NAME, cl))
     )

     actions = ActionChains(driver)

     actions.click(other_place)


     upgrade_actions = ActionChains(driver)
     upgrade_actions.move_to_element(captcha)
     upgrade_actions.click()
     upgrade_actions.perform()

def Allow_cookies(driver):
     WebDriverWait(driver,20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,'//*[@id="gdpr-consent-notice"]')))
     WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="save"]'))).click()


Captcha_Bypass(driver)
Allow_cookies(driver)

# [baden-wuerttemberg, bayern, hessen, niedersachsen, nordrhein-westfalen, rheinland-pfalz, thueringen]

time.sleep(10)

all_links = driver.find_elements_by_class_name('result-list-entry__brand-logo-container')
for link in all_links:
     link.click()
     time.sleep(10)
     multiple_elements = driver.find_elements_by_class_name('breadcrumb__link')
     choose_states = []
     for i in multiple_elements:
          choose_states.append(i.text)
     
     state = choose_states[1]
     scout_id = driver.find_element_by_class_name('is24-scoutid__content padding-top-s').text

     address = driver.find_element_by_class_name('zip-region-and-country').text

     grids = []
     grid_values = driver.find_elements_by_class_name('grid')
     

     print(multiple_elements)
     print(state)
     break



# //*[@id="result-xl-129280384"]/div[1]/a[1]
# //*[@id="result-xl-128580468"]/div[1]/a[1]