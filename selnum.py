from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
import random
from datetime import datetime
import json

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

time.sleep(5)

num_of_pages = driver.find_element_by_css_selector('.p-items:nth-child(7) a').text
print('Num of pages : ', num_of_pages)
All_data_list = []
for page in range(1, int(num_of_pages)):
     print('Page : ', page)
     names = []
     driver.implicitly_wait(5)
     if page == 1:
          all_links = driver.find_elements_by_css_selector('.maxtwolinerHeadline')
     else:
          all_links = driver.find_elements_by_css_selector('#resultListItems .font-regular')

     for n in all_links:
          names.append(n.text)

     print('Length : ', len(names))
     print(names)

     for name in names[:2]:

          link = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.LINK_TEXT, name)))

          link.click()
          data_dict = {}
          try:
               link_header = link.get_attribute('href')
          except:
               link_header = ""

          try:
               modal_popup = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="is24-expose-modal"]/div/div/div/div/div/div[2]/button'))
               )
               modal_popup.click()
          except:
               pass

          time.sleep(3)
          
          multiple_elements = driver.find_elements_by_class_name('breadcrumb__link')
          choose_states = []
          for i in multiple_elements:
               choose_states.append(i.text)

          state = choose_states[1]

          try:
               scout_id = driver.find_element_by_xpath('//*[@id="is24-content"]/div[2]/div/div[3]/div/div/div').text
          except:
               scout_id = ""

          try:
               address = driver.find_element_by_class_name('zip-region-and-country').text
          except:
               address = ""

          try:
               grid_keys = []
               grid_values = []
               grid_content = driver.find_elements_by_css_selector('.two-fifths , .three-fifths')
               
               for i, grid in enumerate(grid_content):
                    if i%2 == 0:
                         grid_keys.append(grid.text)
                         
                    else:
                         grid_values.append(grid.text)
                         

               grids = {}
               for k, v in zip(grid_keys, grid_values):
                    grids[k] = v
          except:
               Print('Grid data is not present')
               pass
               

          try:
               objectb = driver.find_element_by_css_selector('.is24qa-objektbeschreibung-label').text
               objectb_text = driver.find_element_by_css_selector('.is24qa-objektbeschreibung').text
               grids[objectb] = objectb_text
          except:
               pass

          data_dict['Link_Header_Project_Name'] = name
          data_dict['State'] = state
          data_dict['Link_Header_project_Url'] = link_header
          data_dict['Scout id'] = scout_id
          data_dict['Address'] = address
          data_dict['Timestamp'] = datetime.now()
          data_dict['Data'] = grids
               
          All_data_list.append(data_dict)
          with open('Kaufen_Anlageobjekte.json', mode='w', encoding='utf-8') as f:
               json.dump([], f)

          with open('Kaufen_Anlageobjekte.json', mode='w', encoding='utf-8') as feedsjson:
               json.dump(All_data_list, feedsjson, indent=4, default=str)

          driver.back()

     next_page = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.is24-icon-chevron-right.vertical-center')))
     next_page.click()

     





#//*[@id="is24-content"]/div[3]/div[1]/div[2]/dl[1]/dt
#//*[@id="is24-content"]/div[3]/div[1]/div[2]/dl[2]/dt

#//*[@id="is24-content"]/div[3]/div[1]/div[2]/dl[1]

# //*[@id="result-xl-129280384"]/div[1]/a[1]
# //*[@id="result-xl-128580468"]/div[1]/a[1]