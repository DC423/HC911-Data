# HC911-Data

HC911-Data is a Python-based project that captures and stores data from HC911 in a SQLite database, facilitating long-term data storage, querying, and analysis. Initially created to integrate data for Slack feeds, this project now emphasizes robust data handling and storage solutions.

## Table of Contents

	•	Overview
	•	Features
	•	Getting Started
	•	Usage
	•	Contributing
	•	License

## Overview

The HC911-Data project is part of DC423’s efforts to maintain and analyze HC911 information in a structured database, aiming to:
	•	Collect and store incoming HC911 data in a SQLite database.
	•	Enable data visualization and reporting via integrated scripts.
	•	Offer an extendable codebase for additional data integrations and outputs.

## Features

	•	Data Storage: Stores HC911 data in a SQLite database (hc911.db).
	•	Graphing Utilities: Scripts for data visualization by date and type (graph_date.py, graph_types.py).
	•	Modular Design: Easily add or modify data processing functions.

## Getting Started

# Prerequisites

	•	Python 3.x
	•	SQLite3

## Installation

# Clone the repository:
```
git clone https://github.com/DC423/HC911-Data.git
cd HC911-Data
```

# Install Dependencies:

```
pip install sqlite3
```


# Run Data Scripts (Optional for Testing):
- Data Ingestion: python hc911_data.py
- Visualization: python graph_date.py or python graph_types.py

## Usage

### After running hc911_data.py, data is stored in hc911.db. You'll want to set up a cron job to run every minute to get the new data. Here is an example cron tab to run on a RaspberryPi
```
* * * * * /usr/bin/python3 /home/pi/HC911-Data/hc911_data.py
```


### To visualize or analyze data, use the graphing scripts provided:

- Date-based Graphing: python graph_date.py
- Type-based Graphing: python graph_types.py

## Contributing

We welcome contributions! Connect with us on Slack, fork the repo, create a branch, and submit a PR.

## License

This project is licensed under the MIT License.

