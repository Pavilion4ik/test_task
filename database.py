from datetime import datetime

import pandas as pd
import sqlite3

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('https://www.dropbox.com/s/098o6814h5qay7f/data.csv?dl=1', delimiter=";")
df["date"] = [datetime.fromtimestamp(x) for x in df["timestamp"]]
# Create a connection to the SQLite database
conn = sqlite3.connect('events.db')

# Write the DataFrame to the database table
df.to_sql('events', conn, if_exists='replace', index=False)

# Close the database connection
conn.close()
