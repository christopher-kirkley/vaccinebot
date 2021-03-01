from selenium import webdriver
from selenium import common
from selenium.webdriver.firefox.options import Options
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
    time.sleep(2)
    res = ''
    try:
        res = driver.find_element_by_xpath("//div[@class='errormessage']/span").text
    except common.exceptions.NoSuchElementException:
        pass

    if len(res) > 0:
        print(f'{timestamp()} - No appointments.')
    else:
        content=f'Vaccine appointments at convention center currently available, at the following link: {url}. Reply with STOP to opt out of these messages.'
        
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

if __name__ == '__main__':
    while True:
        convention_center()
        time.sleep(300)

