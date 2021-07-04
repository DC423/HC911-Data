import sqlite3
import time
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dateutil import parser
from itertools import groupby


# open hc911.db
conn = sqlite3.connect('hc911.db')
c = conn.cursor()

# used for testing so not really needed but keeping as an example 
def read_from_db():
    c.execute('SELECT time FROM events WHERE type LIKE \'%hooting%\'')
    data = c.fetchall()
    print(data)
    for row in data:
        print(row)

# Function to create a graph for 2021 Data, Change the SQLite query as needed
def graph_data():
    c.execute('SELECT time FROM events WHERE time LIKE \'/2021%\' AND type LIKE \'%hooting%\' AND responder like \'%FD%\'')
    data = c.fetchall()
    # variable setups 
    dates = []
    d2 = []
    values = []
    
    # add the dates to a list 
    for row in data:
        dates.append(row[0].split()[0])
    # use those dates to create the x (d2) and y (values)
    for row in dates: 
         # iterate through the data to sort the data and make it uniqe data
         for value, repeated in groupby(sorted(row)):
            d2.append(parser.parse(row))
            values.append(sum(1 for _ in repeated))

    # setup the graph 
    ax = plt.subplot(111)
    ax.set(xlabel='Dates', ylabel='Shootings Count',
       title='Shootings By Date')
    ax.bar(d2, values)
    ax.xaxis_date()
    plt.show()
    
#read_from_db()
graph_data()
c.close
conn.close()
