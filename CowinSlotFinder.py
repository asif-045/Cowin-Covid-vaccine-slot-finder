import requests
import json
from datetime import datetime
import easygui
import webbrowser
import time
import sys
ProdUrl = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?"

headers = {'Accept': 'application/json',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
           }
PinCode = "743337" #Enter your pincode here
CheckAfter = 1 # Specify your time limit after which you want to check in minutes
VaccineType = "COVAXIN" # Set your vaccine type acceptable values COVISHIELD and COVAXIN
MyAge = 55 # Set your age here, there are different sessions for people having age 45+ and below


def SlotChecker():
    
    x = datetime.now()
    Day = str(x.day)
    Month = str(x.month)
    Year = str(x.year)
    FetchUrl = ProdUrl + "pincode=" + PinCode + "&date=" + Day + "-" + Month + "-" + Year
    ApiResponse = requests.get(FetchUrl, headers = headers)
    # D = '''
    #     {"centers":[{"center_id":590665,"name":"Jaynagar Majilpur MCWC","address":"Jaynagar Majilpur","state_name":"West Bengal","district_name":"South 24 Parganas","block_name":"Joynagar Majilpur Municipality","pincode":743337,"lat":22,"long":88,"from":"10:00:00","to":"17:00:00","fee_type":"Free","sessions":[{"session_id":"ec271094-df35-416b-8375-101cfa63b156","date":"18-05-2021","available_capacity":0,"min_age_limit":45,"vaccine":"COVISHIELD","slots":["10:00AM-12:00PM","12:00PM-02:00PM","02:00PM-04:00PM","04:00PM-05:00PM"],"available_capacity_dose1":0,"available_capacity_dose2":0},{"session_id":"4ee37499-fefd-46cd-9a71-2051c2fc717f","date":"20-05-2021","available_capacity":0,"min_age_limit":45,"vaccine":"COVISHIELD","slots":["10:00AM-12:00PM","12:00PM-02:00PM","02:00PM-04:00PM","04:00PM-05:00PM"],"available_capacity_dose1":0,"available_capacity_dose2":0},{"session_id":"94a08aff-294b-4522-8a4d-43d7b424e755","date":"24-05-2021","available_capacity":0,"min_age_limit":45,"vaccine":"COVISHIELD","slots":["10:00AM-12:00PM","12:00PM-02:00PM","02:00PM-04:00PM","04:00PM-05:00PM"],"available_capacity_dose1":0,"available_capacity_dose2":0}]},{"center_id":558968,"name":"Nimpith S C","address":"SRKRH","state_name":"West Bengal","district_name":"South 24 Parganas","block_name":"Joynagar-II","pincode":743337,"lat":22,"long":88,"from":"10:00:00","to":"17:00:00","fee_type":"Free","sessions":[{"session_id":"4c33ed01-08f8-44f3-86a5-f7c734a58467","date":"18-05-2021","available_capacity":0,"min_age_limit":45,"vaccine":"COVAXIN","slots":["10:00AM-12:00PM","12:00PM-02:00PM","02:00PM-04:00PM","04:00PM-05:00PM"],"available_capacity_dose1":0,"available_capacity_dose2":0}]},{"center_id":556058,"name":"Nimpith S/C","address":"SRKRH","state_name":"West Bengal","district_name":"South 24 Parganas","block_name":"Joynagar-II","pincode":743337,"lat":22,"long":88,"from":"10:00:00","to":"17:00:00","fee_type":"Free","sessions":[{"session_id":"f054a467-d66a-4e22-9ab0-9060a32c7878","date":"18-05-2021","available_capacity":0,"min_age_limit":45,"vaccine":"COVISHIELD","slots":["10:00AM-12:00PM","12:00PM-02:00PM","02:00PM-04:00PM","04:00PM-05:00PM"],"available_capacity_dose1":0,"available_capacity_dose2":0}]}]}
    # '''
    # Data = json.loads(D)
    Data = json.loads(ApiResponse.text)

    if(len(Data['centers'])) <= 0:
        print("No slots available.")
        sys.exit()

    for c in Data['centers']:
        for s in c['sessions']:
            if (MyAge >= s['min_age_limit'] and s['vaccine'] == VaccineType.upper()) and (s['available_capacity'] > 0):
                # we have got an availability
                MsgText = "We have found an availability at "+ c['name'] + " for age " + str(s['min_age_limit']) + "+ and vaccine type "+ s['vaccine'] + ". Current available capacity is " + str(s['available_capacity']) + " Do you want to book now ?"
                UserInput = easygui.ynbox(MsgText, 'Cowin Slot Finder (Author: Rajan Shah)', ('Yes', 'No'))
                if(UserInput):
                    webbrowser.open("https://www.cowin.gov.in/home")
                    sys.exit()
                sys.exit()
        print("No slots available in %s." % (c['name'],), end = ' ')
    return 0

while(True):
    SlotChecker()
    print("Last checked at %s " % (str(datetime.now().time()),))
    print("We'll check again in %s minute(s)" % (CheckAfter,))
    time.sleep(CheckAfter*60)
