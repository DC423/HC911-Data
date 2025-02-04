#
#  Author: Ben Stoker
#  Original Author: Stephen Hilt
#  Purpose: To convert hc911.org alerts to SQLite database entries
#  Version: 0.2
#  Notes: (4/19/2018) Initial Build
#         (11/15/2024) merged with the slack tools one that has the new URL
#         (12/03/2024) Updated to include additional fields from the API response
#         (02/04/2025) Added custom headers (Content-Type, X-Frontend-Auth, Origin) 
#                      to match the JavaScript fetch request for API security and CORS compliance
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

# Function to insert data into the SQLite database
def post_sqlite(time, type, event, responder, area, address, latitude, longitude, city, state, priority, agency_type, battalion):
    conn = sqlite3.connect('hc911.db')
    c = conn.cursor()
    # Insert event data into the database
    c.execute('''
        INSERT INTO events (
            time, type, event, responder, area, address, 
            latitude, longitude, city, state, priority, agency_type, battalion
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (time, type, event, responder, area, address, latitude, longitude, city, state, priority, agency_type, battalion))
    conn.commit()
    conn.close()

# Change a list to a string
def listToString(s):
    str1 = " "
    return str1.join(s)

# URL and API Setup
url = "https://hc911server.com/api/calls"

# Add Custom Headers (Matching the JavaScript Fetch Request)
headers = {
    "Content-Type": "application/json",
    "X-Frontend-Auth": "my-secure-token",  # Required for security
    "Origin": "https://www.hamiltontn911.gov"  # Helps with CORS and verification
}

# Make the GET request with headers
response = requests.get(url, headers=headers)

# Get the current time in 24-hour format
hour = strftime("%H")
min = int(strftime("%M")) - 5
if min < 0:
    min = 60 - abs(min)
    hour = str(int(hour) - 1)
min = "{0:0=2d}".format(min)

# Process each event in the API response
for dic in response.json():
    # Extract and format the creation time
    time = dic['creation']
    newtime = time.split("T")[1]
    n_year = time.split("T")[0]
    n_hour = newtime.split(":")[0]
    n_min = newtime.split(":")[1]
    n_seconds = newtime.split(":")[2].split(".")[0]
    time = f"{n_year} {n_hour}:{n_min}:{n_seconds}"

    # Extract additional fields from the API response
    type = dic['type_description']
    event = dic['status']
    responder = dic['jurisdiction']
    area = dic['crossstreets']
    address = dic['location']
    latitude = dic.get('latitude', None)
    longitude = dic.get('longitude', None)
    city = dic.get('city', None)
    state = dic.get('state', None)
    priority = dic.get('priority', None)
    agency_type = dic.get('agency_type', None)
    battalion = dic.get('battalion', None)

    # Check if the event matches the time criteria
    if n_hour == str(hour) and n_min == str(min):
        post_sqlite(time, type, event, responder, area, address, latitude, longitude, city, state, priority, agency_type, battalion)
