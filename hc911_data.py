#!/usr/bin/python
#
#  Author: Ben Stoker
#  Original Author: Stephen Hilt
#  Purpose: To convert hc911.org alerts to SQLite database entries
#  Version: 0.1
#  Notes: (4/19/2018) Initial Build
#         (11/15/2024) merged with the slack tools one that has the new URL
#
########################################
from pprint import pprint
from time import strftime
import requests
import datetime
import time
import sys
import os
import re
import sqlite3

# also post to sqllite.db 
def post_sqlite(time, type, event, responder, area, address):
    conn = sqlite3.connect('hc911.db')
    c = conn.cursor()
    c.execute('INSERT INTO events (time, type, event, responder, area, address) VALUES (?,?,?,?,?,?)', (time, type, event, responder, area, address))
    conn.commit()
    conn.close()

  
#Change a list to a string, might need to do this a few times 
def listToString(s):
    # initialize an empty string
    str1 = " "
    # return string 
    return (str1.join(s))

#URL AND API SETUP
#New Website as of 2022-09-06
url = "https://hc911server.com/api/calls"
#GET the website from requests
response = requests.get(url)

#Get 24 hour time for Hour of the current time
hour = strftime("%H")
# minute minus 5, the time between 'created_str' and current time is around a 5min delta
min = int(strftime("%M")) -5
# if after the -5 we have a negative number then we need to make this the previous hour
if min < 0:
        min = 60 - abs(min)
        hour = str(int(hour) - 1)
min = "{0:0=2d}".format(min)
# Look at the response from the GET requests
for dic in response.json():
        # pull the creation time and save it as time 
        time = dic['creation']
        # new time is the changing the date, and time (T) is the seperator 
        newtime = time.split("T")[1]
        # year will be saved as n_year 
        n_year = time.split("T")[0]
        # hour will be saved as n_hour 
        n_hour = newtime.split(":")[0]
        # minutes will be saved as n_min
        n_min = newtime.split(":")[1]
        # seconds will be saved as n_seconds 
        n_seconds = newtime.split(":")[2].split(".")[0]
        # create a time variable to use for the messages 
        time = n_year + " " + n_hour + ":" + n_min + ":" + n_seconds
        # save type_description as type 
        type = dic['type_description']
        # save the status as event
        event = dic['status']
        # save the jurisdiction as responder 
        responder = dic['jurisdiction']
        # save the cross streets as area 
        area = dic['crossstreets']
        # save location as address 
        address = dic['location'] 
 
        # IF the time in hours and minuts match the 5 mins ago hour and min then
        if(n_hour == str(hour)and n_min == str(min)): 
            # insert the event into the SQLite3 database 
            post_sqlite(time, type, event, responder, area, address)
