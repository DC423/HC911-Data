import sqlite3
import time
import datetime
import numpy as np
import matplotlib.pyplot as plt

#connect to the hc911.db 
conn = sqlite3.connect('hc911.db')
c = conn.cursor()

# Graph the Data from the Database
def graph_data():
    # SQLite Query to get the top 10 types for 2021 in this example 
    c.execute('SELECT type,count(type) FROM events WHERE time LIKE \'%/2021%\' GROUP BY type ORDER BY count(type) DESC LIMIT 10 ')
    # Read all results 
    data = c.fetchall()
    # setup lists for the data 
    types = []
    counts = []
    
    # Put the SQLite results into the two lists we will use for graphing 
    for row in data:
        types.append(row[0])
        counts.append(row[1])
        
    # Create and build the Graph 
    ax = plt.subplot(111)
    # Set x label and the Title 
    ax.set(xlabel='Count by Types', title='Top 10 Counts by HC911 Type')
    # set the y ticks to be numbers based on the types 
    ax.set_yticks(np.arange(len(types)))
    # set the y axis lables to be the types 
    ax.set_yticklabels(types)
    # create the graph based off the x and y values from the database
    ax.barh(np.arange(len(types)), counts)
    # show the graph
    plt.show()

# Call the graph function and close the connections to the database. 
graph_data()
c.close
conn.close()
