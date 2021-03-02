from selenium import webdriver
from selenium import common
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

import time
import os
from twilio.rest import Client
from twilio.base import exceptions
from config import *
from datetime import datetime

account_sid = TWILIO_ACCOUNT_SID
auth_token = TWILIO_AUTH_TOKEN

client = Client(account_sid, auth_token)


""" Set up browser """
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

def timestamp():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string

def convention_center():
    """ Scrape legacy/convention center """
    url = 'https://lvc.lhs.org/myhealth/SignupAndSchedule/EmbeddedSchedule?dept=202001001&id=&vt=3324'
    driver.get(url)
    time.sleep(5)
    res = ''
    try:
        res = driver.find_element_by_xpath("//div[@class='errormessage']/span").text
    except common.exceptions.NoSuchElementException:
        pass

    if len(res) > 0:
        print(f'{timestamp()} - No appointments.')
    else:
        content=f'Greetings! Vaccine appointments from Legacy Health at the Oregon Convention Center currently available, at the following link: {url}. Reply with STOP to opt out of these messages.'

def send_sms(content):
    for number in phone_numbers:
        try:
            message = client.messages \
                    .create(
                            body=content,
                            from_=my_number,
                            to=number
                            )
        except exceptions.TwilioRestException:
            pass

walgreens_locations = {
        'walgreens': 'https://www.walgreens.com/findcare/vaccination/covid-19/location-screening'
        }

def walgreens(url):
    driver.get(url)
    time.sleep(1)
    location = driver.find_element_by_id("inputLocation")
    location.clear()
    location.send_keys('97219')
    search_button = driver.find_element_by_xpath("//button[@class='btn']")
    search_button.click()
    time.sleep(1)

    try:
        msg = driver.find_element_by_xpath("//section[@class='mt40 mb40']/div[1]/a/span[2]/p").text

        if msg == 'Appointments unavailable':
            print('No appointments')
        else:
            return True
    except common.exceptions.NoSuchElementException:
        print("Error scraping")
        return False


def costco(url):
    driver.get(url)
    time.sleep(5)
    button = driver.find_element_by_xpath("//a[@class='chevron-row ']")
    button.click()
    time.sleep(3)

    try:
        msg = driver.find_element_by_xpath("//div[@id='SelectEmployeeView']/div[1]/div[1]/div[2]/p[1]/span[1]").text

        if msg == "We're sorry, but no":
            print('No appointments')
        else:
            return True

    except common.exceptions.NoSuchElementException:
        print("Error scraping")
        return False


costco_locations = {
        'costco_aloha': 'https://book-costcopharmacy.appointment-plus.com/ctnqxln8/?e_id=5363',
        'costco_tigard': 'https://book-costcopharmacy.appointment-plus.com/ctnt6bsy/?e_id=5389',
        'costco_hillsboro': 'https://book-costcopharmacy.appointment-plus.com/ctv00k3k/?e_id=5391',
        'costco_portland': 'https://book-costcopharmacy.appointment-plus.com/ctnq90z4/?e_id=5371',
        }



if __name__ == '__main__':
    locations = {}
    for store, url in walgreens_locations.items():
        print(f'trying {store}...')
        appt = walgreens(url)
        if appt == True:
            locations.append(f'{store}: {url}')
    for store, url in costco_locations.items():
        print(f'trying {store}...')
        appt = costco(url)
        if appt == True:
            locations.append(f'{store}: {url}')
        time.sleep(5)
    print(locations)
    if len(locations) > 0:
        string = ''
        for location, url in locations.items():
            string = string + f'{location}'
        content=f'Greetings! Vaccine appointments available at the following locations: {string}. Reply with STOP to opt out of these messages.'
        send_sms(content)



