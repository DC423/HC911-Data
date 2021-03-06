#!/usr/bin/python
#
#  Author: Ben Stoker
#  Original Author: Stephen Hilt
#  Purpose: To convert hc911.org alerts to SQLite database entries
#  Version: 0.1
#  Notes: (4/19/2018) Initial Build
#
########################################
from time import strftime
from lxml import etree
from BeautifulSoup import BeautifulSoup
import urllib
import sys
import sqlite3
# replace slacker with my own postMessage function
def post_sqlite(time, type, event, responder, area, address):
    conn = sqlite3.connect('hc911.db')
    c = conn.cursor()
    c.execute('INSERT INTO events (time, type, event, responder, area, address) VALUES (?,?,?,?,?,?)', (time, type, event, responder, area, address))
    conn.commit()
    conn.close()
# new hc911.org link, changes from json to table format
url = "https://www.hc911.org/active_incidents/echo_public_incidents.php"
# Get and read the Table from hc911.org
u = urllib.urlopen(url)
response = u.read()
# remove some of the HTML tags to get only the address of the event
# pip install beautifulsoup
soup = BeautifulSoup(response)
for a in soup.findAll('a'):
    del a['href']
response = str(soup)
response = response.replace("<a target=\"_blank\"", "")
response = response.replace("<a target=\"_blank\">", "")
response = response.replace("</a>><img src=\"./active_incidents/map-marker-icon.png\" /></a>","")
# table tags is added to help parsing
response = "<table>" + response + "</table>"
# create the hour
hour = strftime("%I").lstrip('0')
#24 hour time needed for am/pm matching of the string from hc911.org
t4hour = strftime("%H")
#if its over 11, then its pm else am
if int(t4hour) > 11:
    mn = "PM"
else:
    mn = "AM"
# minute minus 5, the time between 'created_str' and current time is around a 5min delta
min = int(strftime("%M")) -5
# if after the -5 we have a negative number then we need to make this the previous hour
if min < 0:
    min = 60 - abs(min)
    hour = str(int(hour) - 1)
min = "{0:0=2d}".format(min)
# parse the table
# apt-get install lxml
table = etree.HTML(response).find("body/table")
# iterate rows
rows = iter(table)
# create headers field, this isn't needed but can help with lables if needed
headers = [col.text for col in next(rows)]
next(rows)
for row in rows:
    # values set to the row
    values = [col.text for col in row]
    # manipulation of the time field from the website to compare to current time
    time = values[1]
    date = time.split(" ")
    newtime = date[1].split(":")
    # Who the call is dispached to
    responder = str(values[3])
    # address of the event
    address = str(values[5].strip(">"))
    # rough area of town to give you an idea of where exact address is
    area = str(values[6])
    # if they are enroute, on site, etc
    event = str(values[2])
    # the event type: Accident, Shots fired, etc
    type = str(values[4])
    # Link to google map, however this is always None due to the parsing at this poing, need to fix
    #link = str(values[5])
    if newtime[1] == min:
        if newtime[0] == hour:
            if date[2] == mn:
                post_sqlite(time, type, event, responder, area, address)


sys.exit()
