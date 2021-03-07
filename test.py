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

def timestamp():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string


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
        'Walgreens': 'https://www.walgreens.com/findcare/vaccination/covid-19?ban=covid_vaccine_landing_schedule'
        }

def walgreens(url, driver):
    driver.get(url)
    time.sleep(4)
    try:
        button = driver.find_element_by_xpath("//a[@href='/findcare/vaccination/covid-19/location-screening']")
        button.click()
        time.sleep(4)
        print('button clicked')
        location = driver.find_element_by_id("inputLocation")
        location.clear()
        location.send_keys('97219')
        search_button = driver.find_element_by_xpath("//button[@class='btn']")
        search_button.click()
        print('search location input')
    except common.exceptions.NoSuchElementException:
        print("Error scraping")
        return False

    time.sleep(2)


    if "Appointments unavailable" in driver.page_source:
        print('No appointments')
    else:
        print("appointment!")
        return True


def costco(url, driver):
    driver.get(url)
    time.sleep(5)
    try:
        button = driver.find_element_by_xpath("//a[@class='chevron-row ']")
        button.click()
    except common.exceptions.NoSuchElementException:
        print("Error scraping, no button")
        return False

    time.sleep(3)

    if "sorry" in driver.page_source:
        print('No appointments')
    else:
        return True



costco_locations = {
        'Costco Aloha': 'https://book-costcopharmacy.appointment-plus.com/ctnqxln8/?e_id=5363',
        'Costco Tigard': 'https://book-costcopharmacy.appointment-plus.com/ctnt6bsy/?e_id=5389',
        'Costco Hillsboro': 'https://book-costcopharmacy.appointment-plus.com/ctv00k3k/?e_id=5391',
        'Costco Portland': 'https://book-costcopharmacy.appointment-plus.com/ctnq90z4/?e_id=5371',
        }

def main():
    """ Set up browser """
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    print(timestamp())
    locations = {}
    for store, url in walgreens_locations.items():
        print(f'trying {store}...')
        appt = walgreens(url, driver)
        if appt == True:
            locations[store] = url
    for store, url in costco_locations.items():
        print(f'trying {store}...')
        appt = costco(url, driver)
        if appt == True:
            locations[store] = url
        time.sleep(5)
    if len(locations) > 0:
        print(locations)
        string = ''
        for location, url in locations.items():
            string = string + f'{location}'
        content=f'Greetings! Vaccine appointments available, check the following locations: {string}. Reply with STOP to opt out of these messages.'
        send_sms(content)
    driver.close()


if __name__ == '__main__':
    while True:
        main()
        print('sleeping for 10 min .... ')
        time.sleep(600)




