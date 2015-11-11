import sys
import csv
import logging
import os.path

import phonenumbers
from twilio.rest import TwilioRestClient

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
handler = logging.FileHandler('send.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Twilio Setup
import config
client = TwilioRestClient(config.ACCOUNT, config.TOKEN)

# Get message
happy = "N"
while(happy != "Y" and happy != "y"):
    print "Please enter your message: "
    message_body = raw_input()
    happy = raw_input("Is this message correct? Y/N ")


# Get phone numbers & check config
succes = True
phone_number_dir = ""
while(not os.path.isfile(phone_number_dir) or not succes):
    phone_number_dir = raw_input("Where are the phone numbers? (Default: numbers.csv) " )
    if(phone_number_dir == ""):
        phone_number_dir = "numbers.csv"

        numbers = []
        with open(phone_number_dir, 'rb') as f:
            reader = csv.reader(f)
            for index, row in enumerate(reader):
                try:
                    number =  phonenumbers.format_number(phonenumbers.parse(row[0], "US"), phonenumbers.PhoneNumberFormat.E164)
                except Exception, e:
                    print "Invalid Phone Number at Index: %s %s" % (row[0], str(index))
                    sys.exit(1)
                numbers.append(number)


# Fuck it, Ship it
logger.info("MESSAGE: %s ", message_body)
logger.info("NUMBER_DIRECTORY: %s ", phone_number_dir)
for index, number in enumerate(numbers):
    try:
        message = client.messages.create(to=number, from_=config.PHONE_NUMBER,
                                     body=message_body)
        logger.info("SUCCESS: %s %s", str(index), number)
    except Exception, e:
        logger.info("FAILURE: %s", number)