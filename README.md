# Vaccine Appointment Finder

A minimal Covid vaccine appointment finder. Web scrapes various locations, support for Costco and Walgreens.

## Requirements
- Python 3.7
- Selenium
- Twilio

## Use
Requires a Twilio account for SMS functionality.  

Config should be stored in a `config.py` file, containing the following:  

TWILIO_ACCOUNT_SID=''
TWILIO_AUTH_TOKEN=''
PHONE_NUMBERS=['', '', '']

