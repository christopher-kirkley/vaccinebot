# Vaccine Appointment Finder

A minimal Covid vaccine appointment finder. Web scrapes various locations, support for Costco and Walgreens.

## Requirements
- Python 3.7
- Selenium
- Twilio

## Config
Requires a Twilio account for SMS functionality.   

Config should be stored in a `config.py` file, containing the following:  

TWILIO_ACCOUNT_SID=account_sid  
TWILIO_AUTH_TOKEN=auth_token
PHONE_NUMBERS=[number1, number2]  

## Use

Install requirements  
`python -m pip install -r requirements.txt`

Run
`python bot.py`

Script will runs headless, but will print out some minimal information to console in addition to sending SMS. Scraping repeats every 10 minutes. Script can be modified to change increments, or locations (stored in a dict object in bot.py).

