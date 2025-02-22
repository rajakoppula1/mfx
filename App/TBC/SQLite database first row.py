import sqlite3

# Define the database file path
db_file_path = '/Users/rajasimhakoppula/Downloads/Complete Automation/us_zip_codes.db'

# Connect to the SQLite database
conn = sqlite3.connect(db_file_path)

# Create a cursor object
cursor = conn.cursor()

# Query to select the first row from the table
query = 'SELECT * FROM "us_zip_codes.db" LIMIT 1;'

# Execute the query
cursor.execute(query)

# Fetch the first row
first_row = cursor.fetchone()

# Print the first row
print(first_row)

# Close the cursor and connection
cursor.close()
conn.close()
