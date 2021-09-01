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
from bs4 import BeautifulSoup

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

    for name in names[:5]:

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

        driver.implicitly_wait(5)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        
        try:
            scout_id = soup.select_one('.is24-scoutid__content').get_text(strip=True)
        except:
            scout_id = ""

        try:    
            address = soup.select_one('.zip-region-and-country').get_text(strip=True)
        except:
            address = ""

        try:
            state = soup.select_one('.breadcrumb__item:nth-child(2) .breadcrumb__link').get_text(strip=True)
        except:
            state = ""
        
        try:
            gkeys = []
            gvalues = []
            for i, grid in enumerate(soup.select('.two-fifths , .three-fifths')):
                if i % 2 == 0:
                    gkeys.append(grid.get_text(strip=True))
                else:
                    gvalues.append(grid.get_text(strip=True))

            grid_dict = {}
            for k, v in zip(gkeys, gvalues):
                grid_dict[k] = v
        except:
            grid_dict = {}
    

        data_dict['Link_Header_Project_Name'] = name
        data_dict['State'] = state
        data_dict['Link_Header_project_Url'] = link_header
        data_dict['Scout id'] = scout_id
        data_dict['Address'] = address
        data_dict['Timestamp'] = datetime.now()
        data_dict['Data'] = grid_dict
        
        All_data_list.append(data_dict)
        driver.back()

    with open('Kaufen_Anlageobjekte.json', mode='w', encoding='utf-8') as f:
        json.dump([], f)

    with open('Kaufen_Anlageobjekte.json', mode='w', encoding='utf-8') as feedsjson:
        json.dump(All_data_list, feedsjson, indent=4, default=str)


    next_page = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.is24-icon-chevron-right.vertical-center')))
    next_page.click()

     





#//*[@id="is24-content"]/div[3]/div[1]/div[2]/dl[1]/dt
#//*[@id="is24-content"]/div[3]/div[1]/div[2]/dl[2]/dt

#//*[@id="is24-content"]/div[3]/div[1]/div[2]/dl[1]

# //*[@id="result-xl-129280384"]/div[1]/a[1]
# //*[@id="result-xl-128580468"]/div[1]/a[1]