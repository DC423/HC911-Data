import sqlite3
import datetime
from collections import defaultdict
import matplotlib.pyplot as plt

# Connect to the hc911.db
conn = sqlite3.connect('hc911.db')
c = conn.cursor()

def graph_event_type_trend(event_type):
    # Fetch all rows matching the event type
    query = """
    SELECT time, address
    FROM events
    WHERE LOWER(type) LIKE ?
    """
    c.execute(query, (f"%{event_type.lower()}%",))
    rows = c.fetchall()
    
    # Initialize year counts
    year_counts = defaultdict(int)
    current_year = datetime.datetime.now().year
    time_window = datetime.timedelta(minutes=5)  # Define a 5-minute grouping window
    
    # Dictionary to track the last recorded event per address
    address_last_event = defaultdict(lambda: datetime.datetime.min)
    
    # Process each row
    for row in rows:
        raw_time, address = row
        if not raw_time or not address:
            continue
        
        # Parse the time value
        try:
            # Attempt to parse the new format (YYYY-MM-DD HH:MM:SS)
            event_time = datetime.datetime.strptime(raw_time, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            try:
                # Attempt to parse the old format (MM/DD/YYYY HH:MM:SS AM/PM)
                event_time = datetime.datetime.strptime(raw_time, "%m/%d/%Y %I:%M:%S %p")
            except ValueError:
                continue
        
        # Extract the event year
        year = event_time.year
        
        # Skip out-of-bounds years
        if not (2000 <= year <= current_year + 5):
            continue
        
        # Check if the event is within the time window for the same address
        last_event_time = address_last_event[address]
        if event_time - last_event_time <= time_window:
            # Skip this event as it's within the same time window
            continue
        
        # Record the event and update the last event time for the address
        year_counts[year] += 1
        address_last_event[address] = event_time
    
    # Prepare data for graphing
    sorted_years = sorted(year_counts.keys())
    counts = [year_counts[year] for year in sorted_years]
    
    # If no valid data, show a warning
    if not sorted_years:
        print(f"No valid data found for event type '{event_type}'.")
        return
    
    # Create and build the graph
    plt.figure(figsize=(10, 6))
    plt.plot(sorted_years, counts, marker='o', linestyle='-', color='b')
    plt.title(f"Year-Over-Year Trend for '{event_type.title()}' (Unique by Address/Time)")
    plt.xlabel("Year")
    plt.ylabel("Count")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Example Usage
if __name__ == "__main__":
    event_type_input = input("Enter the event type to search for (e.g., 'shooting'): ").strip()
    if event_type_input:
        graph_event_type_trend(event_type_input)
    else:
        print("No event type provided. Exiting.")
    c.close()
    conn.close()
