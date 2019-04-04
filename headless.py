from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import json
import requests
import random


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


session_cicle_count = 1

while True:
    data = json.loads(requests.get(
        'https://randomuser.me/api/').text)["results"][0]

    first_name = data['name']['first'].capitalize()
    last_name = data['name']['last'].capitalize()
    email = new_email_address(data['email'])
    cell = new_phone_number()
    zip_code = data['location']['postcode']

    print(
        f'Cicle number {session_cicle_count}\nCurently using:\n{first_name} {last_name}\n{email}\n+1 {cell}\nZIP: {zip_code}\n\n')

    chrome_options = Options()
    chrome_options.add_argument("headless")
    chrome_options.add_argument("--window-size=1920x1080")

    maildriver = webdriver.Chrome(
        './chromedriver', chrome_options=chrome_options)
    maildriver.get(f"https://shitmail.me/mail/inbox/{email}")
    wait = WebDriverWait(maildriver, 600)

    flumedriver = webdriver.Chrome(
        './chromedriver', chrome_options=chrome_options)
    flumedriver.get("https://arep.co/xJbFWz/register")
    wait = WebDriverWait(flumedriver, 600)

    try:
        time.sleep(2)

        # Input email
        email_box = flumedriver.find_elements_by_xpath(
            '//*[@id="__layout"]/div/main/div/section/div[1]/form/div[1]/div[1]/input')[0]
        email_box.click()
        email_box.send_keys(email)

        # Input first and last name
        fname_box = flumedriver.find_elements_by_xpath(
            '//*[@id="firstName"]')[0]
        fname_box.click()
        fname_box.send_keys(first_name)

        lname_box = flumedriver.find_elements_by_xpath(
            '//*[@id="lastName"]')[0]
        lname_box.click()
        lname_box.send_keys(last_name)

        # Select country code and input phone number
        flumedriver.find_element_by_tag_name("body").send_keys(Keys.TAB)
        for i in range(0, random.randint(1, 20)):
            flumedriver.find_element_by_tag_name(
                "body").send_keys(Keys.ARROW_DOWN)
        flumedriver.find_element_by_tag_name("body").send_keys(Keys.ENTER)
        time.sleep(1)
        phone_box = flumedriver.find_elements_by_xpath(
            '//*[@id="__layout"]/div/main/div/section/div[1]/form/div[2]/div/div[1]/section[2]/input')[0]
        phone_box.click()
        phone_box.send_keys(cell)

        # Input zip code
        zip_box = flumedriver.find_elements_by_xpath(
            '//*[@id="__layout"]/div/main/div/section/div[1]/form/div[3]/div/input')[0]
        zip_box.click()
        zip_box.send_keys(zip_code)

        # Submit
        flumedriver.find_elements_by_xpath(
            '//*[@id="__layout"]/div/div[2]/div/div[2]/button/span')[0].click()

        time.sleep(5)
        flumedriver.quit()


        # Refresh inbox
        maildriver.refresh()
        time.sleep(3)
        inboxmail = maildriver.find_elements_by_xpath(
            '/html/body/div[2]/table/tbody/tr[1]/td[3]/a')[0]
        time.sleep(3)

        # Get verification url
        oldurl = inboxmail.get_attribute("href")
        print(f'Successfully got {insecure_url(oldurl)}')
        maildriver.quit()
        

        # Verify mail address
        verificationdriver = webdriver.Chrome(
            './chromedriver', chrome_options=chrome_options)
        verificationdriver.get(insecure_url(oldurl))
        wait = WebDriverWait(verificationdriver, 600)
        time.sleep(4)
        verificationdriver.find_elements_by_xpath(
            '/html/body/table/tbody/tr[3]/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/a')[0].click()
        time.sleep(5)
        verificationdriver.quit()



        print(f'\nCicle {session_cicle_count} successfully completed\n-----------\n')
        session_cicle_count += 1
    except Exception as ex:
        print(f'{ex}\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!\nError during cicle {session_cicle_count}, retrying\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')
        try:
            maildriver.quit()
            flumedriver.quit()
            verificationdriver.quit()
        except:
            pass
