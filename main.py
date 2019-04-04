from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import json
import requests
import random
import sys


def new_phone_number():
    phone_number = ""
    for i in range(0, 9):
        phone_number += str(random.randint(0, 9))
    return phone_number


def new_email_address(tomodify):
    email_address = ""
    for i in range(0, len(tomodify)):
        if tomodify[i] == '@':
            email_address = f'{tomodify[0:i]}@shitmail.me'
    return email_address


def insecure_url(secure):
    return secure.replace("plain", "html")


session_cycle_count = 1
standard_wait_time = 1
instance_number = sys.argv[1]

while True:
    data = json.loads(requests.get(
        'https://randomuser.me/api/').text)["results"][0]

    first_name = data['name']['first'].capitalize()
    last_name = data['name']['last'].capitalize()
    email = new_email_address(data['email'])
    cell = new_phone_number()
    zip_code = data['location']['postcode']

    print(f'Instance {instance_number} - Starting cycle {session_cycle_count}')

    chrome_options = Options()
    chrome_options.add_argument("headless")
    chrome_options.add_argument("--window-size=1920x1080")

    driver = webdriver.Chrome(
        './chromedriver', chrome_options=chrome_options)
    driver.get(f"https://shitmail.me/mail/inbox/{email}")
    wait = WebDriverWait(driver, 600)
    time.sleep(2)
    driver.get("https://arep.co/xJbFWz/register")
    wait = WebDriverWait(driver, 600)

    # Input email
    didpass = False
    while didpass is False:
        try:
            didpass = True
            time.sleep(2)
            email_box = driver.find_elements_by_xpath(
                '//*[@id="__layout"]/div/main/div/section/div[1]/form/div[1]/div[1]/input')[0]
            email_box.click()
            email_box.send_keys(email)
        except:
            print(f"Instance {instance_number} - Failed in input email")
            didpass = False


    # Input first and last name
    didpass = False
    while didpass is False:
        try:
            didpass = True
            fname_box = driver.find_elements_by_xpath(
                '//*[@id="firstName"]')[0]
            fname_box.click()
            fname_box.send_keys(first_name)
        except:
            print(f"Instance {instance_number} - Failed in input first name")
            time.sleep(standard_wait_time)
            didpass = False

    didpass = False
    while didpass is False:
        try:
            didpass = True
            lname_box = driver.find_elements_by_xpath(
                '//*[@id="lastName"]')[0]
            lname_box.click()
            lname_box.send_keys(last_name)
        except:
            print(f"Instance {instance_number} - Failed in input last name")
            time.sleep(standard_wait_time)
            didpass = False

    # Select country code and input phone number
    didpass = False
    while didpass is False:
        try:
            didpass = True
            driver.find_element_by_tag_name("body").send_keys(Keys.TAB)
            for i in range(0, random.randint(1, 20)):
                driver.find_element_by_tag_name(
                    "body").send_keys(Keys.ARROW_DOWN)
            driver.find_element_by_tag_name("body").send_keys(Keys.ENTER)
        except:
            print(f"Instance {instance_number} - Failed in select country code")
            time.sleep(standard_wait_time)
            didpass = False
    didpass = False
    while didpass is False:
        try:
            didpass = True
            phone_box = driver.find_elements_by_xpath(
                '//*[@id="__layout"]/div/main/div/section/div[1]/form/div[2]/div/div[1]/section[2]/input')[0]
            phone_box.click()
            phone_box.send_keys(cell)
        except:
            print(f"Instance {instance_number} - Failed in input phone number")
            time.sleep(standard_wait_time)
            didpass = False

    # Input zip code
    didpass = False
    while didpass is False:
        try:
            didpass = True
            zip_box = driver.find_elements_by_xpath(
                '//*[@id="__layout"]/div/main/div/section/div[1]/form/div[3]/div/input')[0]
            zip_box.click()
            zip_box.send_keys(zip_code)
        except:
            print(f"Instance {instance_number} - Failed in input ZIP")
            time.sleep(standard_wait_time)
            didpass = False

    # Submit
    didpass = False
    while didpass is False:
        try:
            didpass = True
            driver.find_elements_by_xpath(
                '//*[@id="__layout"]/div/div[2]/div/div[2]/button/span')[0].click()
        except:
            print(f"Instance {instance_number} - Failed in submit")
            time.sleep(standard_wait_time)
            didpass = False

    time.sleep(5)
    driver.get(f"https://shitmail.me/mail/inbox/{email}")

    # Refresh inbox and
    didpass = False
    while didpass is False:
        try:
            didpass = True
            driver.refresh()
            inboxmail = driver.find_elements_by_xpath(
                '/html/body/div[2]/table/tbody/tr[1]/td[3]/a')[0]
            oldurl = inboxmail.get_attribute("href")
        except:
            print(f"Instance {instance_number} - Failed in find email in inbox")
            time.sleep(standard_wait_time)
            didpass = False

    # Verify mail address
    driver.get(insecure_url(oldurl))
    wait = WebDriverWait(driver, 600)
    didpass = False
    while didpass is False:
        try:
            didpass = True
            driver.find_elements_by_xpath(
                '/html/body/table/tbody/tr[3]/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/a')[0].click()
            time.sleep(5)
        except:
            print(f"Instance {instance_number} - Failed in verify")
            time.sleep(standard_wait_time)
            didpass = False
    driver.quit()

    print(f'\n--Instance {instance_number} - Cycle {session_cycle_count} success {first_name} {last_name}--\n')
    session_cycle_count += 1
