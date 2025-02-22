import sqlite3

# File path to your SQLite database
db_path = '/Users/rajasimhakoppula/Documents/mfx/App/PRAG/data/spatial_analysis.db'

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Print table names and their columns with data types
for table in tables:
    table_name = table[0]
    print(f"Table: {table_name}")
    
    # Retrieve column information
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    
    # Print each column's name and data type
    for col in columns:
        col_name, col_type = col[1], col[2]
        print(f" - Column: {col_name}, Type: {col_type}")
    print()

# Close the connection
conn.close()
