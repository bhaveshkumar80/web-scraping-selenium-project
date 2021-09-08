from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import time
import random
from datetime import datetime
import json
from bs4 import BeautifulSoup
import os

opts = Options()
opts.add_argument("user-agent=whatever you want")

opts.add_argument('--ignore-certificate-errors')
opts.add_argument('--ignore-ssl-errors')


def page_counter(file_name, url, json_data_list = [], nth_element = 0, start_page = 1):

    if os.path.isfile(file_name):
        with open(file_name, 'r') as f:
            json_data_list = json.load(f)

        start_page = int(len(json_data_list) // 20) + 1
        if len(json_data_list) >= 20:
            url = url + '?pagenumber=' + str(start_page)


        nth_element = int(len(json_data_list) % 20)

        return url, json_data_list, nth_element, start_page

    else:
        with open(file_name, mode='w', encoding='utf-8') as f:
            json.dump([], f)

        return url, json_data_list, nth_element, start_page

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

def Selenium_scraper(url, file_name, json_data_list, start_page, nth_element, driver):

    bypass = 0
    while True:
        try:
            Captcha_Bypass(driver)
            Allow_cookies(driver)
            bypass = 1
        except:
            driver.get(url)
            pass

        if bypass == 1:
            break

    # [baden-wuerttemberg, bayern, hessen, niedersachsen, nordrhein-westfalen, rheinland-pfalz, thueringen]

    driver.implicitly_wait(5)

    try:
        num_of_pages = int(driver.find_element_by_css_selector('.p-items:nth-child(7) a').text)
    except:
        try:
            num_of_pages = int(driver.find_element_by_css_selector('.p-items:nth-child(8) a').text)
        except:
            try:
                num_of_pages = int(driver.find_element_by_css_selector('.p-active+ .p-items a').text)
            except:
                num_of_pages = int(driver.find_element_by_css_selector('.p-active a').text)

    print('Num of pages : ', num_of_pages)

    for page in range(start_page, int(num_of_pages)):
        print('Page : ', page)
        names = []
        driver.implicitly_wait(5)
        #if page == 1:
        all_links = driver.find_elements_by_css_selector('a .maxtwolinerHeadline')
        #else:
        #    all_links = driver.find_elements_by_css_selector('#resultListItems .font-regular')

        for n in all_links:
            names.append(n.text)

        print('Length : ', len(names))
        print(names)

        if start_page != page:
            nth_element = 0

        for name in names[nth_element:]:
            
            try:
                link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, name)))
            except:
                continue

            data_dict = {}
            try:
                link_header = link.get_attribute('href')
            except:
                link_header = ""

            if link_header.split('.')[-1] == 'html':
                continue

            link.click()

            # try:
            #     modal_popup = WebDriverWait(driver, 15).until(
            #             EC.presence_of_element_located((By.XPATH, '//*[@id="is24-expose-modal"]/div/div/div/div/div/div[2]/button'))
            #     )
            #     modal_popup.click()
            # except:
            #     pass

            driver.implicitly_wait(10)
            soup = BeautifulSoup(driver.page_source, 'lxml')
            
            try:
                scout_id = soup.select_one('.is24-scoutid__content').get_text(strip=True)
            except:
                scout_id = ""

            try:    
                address = soup.select_one('.zip-region-and-country').get_text(strip=True)
            except:
                address = ""
            
            grid_dict = {}
            try:
                parameter_list = soup.select('dl.grid')
                for l in parameter_list:
                    try:
                        tag = l.select_one('dt').get_text(strip=True)
                        val = l.select_one('dd').get_text(strip=True)
                        grid_dict[tag] = val
                    except:
                        continue
            except:
                pass

            try:
                objectb = soup.select_one('.is24qa-objektbeschreibung-label').get_text(strip=True)
                objectb_text = soup.select_one('.is24qa-objektbeschreibung').get_text(strip=True)
                grid_dict[objectb] = objectb_text
            except:
                pass

            data_dict['Link_Header_Project_Name'] = name
            data_dict['State'] = url.split('/')[-2]
            data_dict['Link_Header_project_Url'] = link_header
            data_dict['Scout id'] = scout_id
            data_dict['Address'] = address
            data_dict['Timestamp'] = datetime.now()
            data_dict['Data'] = grid_dict

            json_data_list.append(data_dict)
            with open(file_name, mode='w', encoding='utf-8') as feedsjson:
                json.dump(json_data_list, feedsjson, indent=4, default=str)

            driver.back()


        next_page = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.is24-icon-chevron-right.vertical-center')))
        next_page.click()

def Append_files(temp_file, main_file):
    with open(temp_file, 'r') as f:
        temp_json = json.load(f)

    if os.path.isfile(main_file):
        with open(main_file, 'r') as f:
            main_json = json.load(f)
    else:
        main_json = []

    append_json = main_json + temp_json

    with open(main_file, 'w') as f:
        json.dump(append_json, f, indent=4, default='str')

    os.remove(temp_file)

url_list = [
            "https://www.immobilienscout24.de/Suche/de/baden-wuerttemberg/haus-kaufen",
            "https://www.immobilienscout24.de/Suche/de/bayern/haus-kaufen",
            "https://www.immobilienscout24.de/Suche/de/berlin/berlin/haus-kaufen",
            "https://www.immobilienscout24.de/Suche/de/brandenburg/haus-kaufen",
            "https://www.immobilienscout24.de/Suche/de/bremen/haus-kaufen",
            "https://www.immobilienscout24.de/Suche/de/hamburg/hamburg/haus-kaufen",
            "https://www.immobilienscout24.de/Suche/de/hessen/haus-kaufen",
            "https://www.immobilienscout24.de/Suche/de/niedersachsen/haus-kaufen",
            "https://www.immobilienscout24.de/Suche/de/mecklenburg-vorpommern/haus-kaufen",
            "https://www.immobilienscout24.de/Suche/de/nordrhein-westfalen/haus-kaufen",
            "https://www.immobilienscout24.de/Suche/de/rheinland-pfalz/haus-kaufen",
            "https://www.immobilienscout24.de/Suche/de/saarland/haus-kaufen",
            "https://www.immobilienscout24.de/Suche/de/sachsen/haus-kaufen",
            "https://www.immobilienscout24.de/Suche/de/sachsen-anhalt/haus-kaufen",
            "https://www.immobilienscout24.de/Suche/de/schleswig-holstein/haus-kaufen",
            "https://www.immobilienscout24.de/Suche/de/thueringen/haus-kaufen"

        ]


def KH():
    main_file = 'Kaufen_Haus.json'

    for url in url_list:
        temp_file = 'temp_' + main_file
        while True:
            try:
                url, json_data_list, nth_element, start_page = page_counter(temp_file, url)

                driver = webdriver.Chrome(chrome_options=opts, executable_path=r'G:\chromedriver.exe')
                driver.get(url)

                Selenium_scraper(url, temp_file, json_data_list, start_page, nth_element, driver)

                Append_files(temp_file, main_file)

                driver.quit()
                break

            except TimeoutException as exception:
                driver.quit()
                continue
