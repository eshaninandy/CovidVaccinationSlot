import requests
import time
import json
from datetime import datetime, timedelta
#from playsound import playsound

# Please change requirements below
age = 46 # Age of the person
pincodes = ['560076', '793002', '793001', '110008'] # Pincode/s to search vaccine availability
num_days = 1 # Number of days in the future to search for

today = datetime.today()
further_days = [today + timedelta(days=i) for i in range(num_days)]
dates = [i.strftime("%d-%m-%Y") for i in further_days]

cnt = 0
i=0
while i<2:
    for pincode in pincodes:
        for date in dates:
            url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(
                pincode, date)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'
                }
            result = requests.get(url, headers = headers)
            if result.ok:
              response_json = result.json()
              flag = False
              if response_json['centers']:
                for center in response_json['centers']:
                  for session in center['sessions']:
                    if session['min_age_limit']<=age and session['available_capacity']>0:
                      print('\nPincode: ' + pincode)
                      print('\nAvailability date: ' + date)
                      print("\nAddress: "+center['address'])
                      print("\nCenter: "+center['name'])
                      print("\nBlock Name: "+center['block_name'])
                      print("\nPrice: "+center['fee_type'])
                      print("\nAvailable capacity (Dose 1): "+str(session['available_capacity_dose1']))
                      print("\nAvailable capacity (Dose 2): "+str(session['available_capacity_dose2']))
                      print("\nVaccine Type: "+session['vaccine'])
                      cnt+=1
            else:
              print("\nIssue with API. No response.")
    if cnt==0:
      print("\nNo vaccine slots available.")
    else:
      print("\nFound vaccine! Please find the details above!")
      print("\nLogin to https://www.cowin.gov.in/home -> Sign in -> Book the vaccine appointment using the details.")
      #playsound("notification_sound.mp3")

    print("\n==================================\n")
    i += 1
