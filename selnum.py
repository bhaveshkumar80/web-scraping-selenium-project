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

     cl = random.choice(['geetest_dot', 'geetest_small', 'geetest_bg', 'geetest_hook', 'geetest_h'])
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

     modal_popup = WebDriverWait(driver, 15).until(
          EC.presence_of_element_located((By.XPATH, '//*[@id="is24-expose-modal"]/div/div/div/div/div/div[2]/button'))
     )
     modal_popup.click()

     time.sleep(5)

     title = driver.find_element_by_xpath('//*[@id="expose-title"]')
     multiple_elements = driver.find_elements_by_class_name('breadcrumb__link')
     choose_states = []
     for i in multiple_elements:
          choose_states.append(i.text)
     
     state = choose_states[1]
     scout_id = driver.find_element_by_xpath('//*[@id="is24-content"]/div[2]/div/div[3]/div/div/div').text

     address = driver.find_element_by_class_name('zip-region-and-country').text

     grids = {}
     grid_values = driver.find_elements_by_xpath('#//*[@id="is24-content"]/div[3]/div[1]/div[2]/dl[1]')
     for grid in grid_values:
          dt = grid.find_element_by_xpath('//*[@id="is24-content"]/div[3]/div[1]/div[2]/dl[1]/dt').text
          dd = grid.find_element_by_xpath('//*[@id="is24-content"]/div[3]/div[1]/div[2]/dl[1]/dd').text
          if dt is not None:
               grids[dt] = dd


     print(title)
     print(state)
     print(scout_id)
     print(address)
     print(grids)
     break


#//*[@id="is24-content"]/div[3]/div[1]/div[2]/dl[1]/dt
#//*[@id="is24-content"]/div[3]/div[1]/div[2]/dl[2]/dt

#//*[@id="is24-content"]/div[3]/div[1]/div[2]/dl[1]

# //*[@id="result-xl-129280384"]/div[1]/a[1]
# //*[@id="result-xl-128580468"]/div[1]/a[1]