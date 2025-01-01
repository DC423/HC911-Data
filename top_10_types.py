import sqlite3
import datetime
import numpy as np
import matplotlib.pyplot as plt

# Connect to the hc911.db
conn = sqlite3.connect('hc911.db')
c = conn.cursor()

# Graph the Data from the Database
def graph_unique_data(date_filter=None, use_pie_chart=False):
    # If no date is passed, use the current year
    if date_filter is None:
        current_year = datetime.datetime.now().year
        date_start = f"{current_year}-01-01 00:00:00"
        date_end = f"{current_year}-12-31 23:59:59"
        print(f"Querying data for the year {current_year}.")
    else:
        # Validate and parse the input date
        try:
            input_date = datetime.datetime.strptime(date_filter, "%Y-%m-%d")
            date_start = input_date.strftime("%Y-%m-%d 00:00:00")
            date_end = input_date.strftime("%Y-12-23 23:59:59")
            #date_end = (input_date + datetime.timedelta(days=1)).strftime("%Y-%m-%d 00:00:00")
            print(f"Querying data for the date {date_filter}.")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return
    
    # SQLite Query to fetch unique event counts by type and address
    query = f"""
    SELECT type, COUNT(*) as unique_event_count
    FROM (
        SELECT type, address, MIN(time) as first_time
        FROM events
        WHERE time BETWEEN '{date_start}' AND '{date_end}'
        GROUP BY type, address
    ) as unique_events
    GROUP BY type
    ORDER BY unique_event_count DESC
    LIMIT 10
    """
    
    # Execute the query
    c.execute(query)
    data = c.fetchall()
    
    # Debug: Print the query result
    print("Query Result:", data)
    
    # Prepare lists for graphing
    types = [row[0] for row in data]
    counts = [row[1] for row in data]
    
    # If no data, show a warning
    if not types:
        print("No data available for the selected period.")
        return
    
    # Choose between Bar Chart or Pie Chart
    if use_pie_chart:
        # Create and build a pie chart
        plt.figure(figsize=(8, 8))
        plt.pie(counts, labels=types, autopct='%1.1f%%', startangle=140)
        plt.title('Top 10 Unique Event Types')
    else:
        # Create and build a bar chart
        fig, ax = plt.subplots()
        sorted_indices = np.argsort(counts)[::-1]  # Sort indices descending
        types_sorted = np.array(types)[sorted_indices]
        counts_sorted = np.array(counts)[sorted_indices]
        ax.barh(np.arange(len(types_sorted)), counts_sorted, color='skyblue')
        ax.set_yticks(np.arange(len(types_sorted)))
        ax.set_yticklabels(types_sorted)
        ax.set(xlabel='Unique Event Count', title='Top 10 Unique Counts by HC911 Type')
        ax.invert_yaxis()  # Largest bar on top
    
    # Show the chart
    plt.show()

# Example Usage
if __name__ == "__main__":
    # User can pass a date in the format YYYY-MM-DD, or leave it blank for the current year
    user_input = input("Enter a date (YYYY-MM-DD) or leave blank for the current year: ").strip()
    chart_type = input("Would you like a pie chart? (yes/no): ").strip().lower()
    use_pie_chart = chart_type in ['yes', 'y']
    
    if user_input:
        graph_unique_data(date_filter=user_input, use_pie_chart=use_pie_chart)
    else:
        graph_unique_data(use_pie_chart=use_pie_chart)
    
    # Close the connection to the database
    c.close()
    conn.close()
