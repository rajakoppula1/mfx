import sqlite3

# File path for the SQLite database
db_path = '/Users/rajasimhakoppula/Documents/mfx/App/PRAG/data/spatial_analysis.db'

def connect_db(db_path):
    """Establish a connection to the SQLite database."""
    return sqlite3.connect(db_path)

def create_tables(conn):
    """Create necessary tables if they do not exist."""
    cursor = conn.cursor()
    
    # Create Locations table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Locations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        country TEXT NOT NULL,
        zip_code TEXT NOT NULL,
        lat REAL NOT NULL,
        long REAL NOT NULL
    )
    """)
    
    # Create UserData table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS UserData (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        zip_code TEXT,
        category TEXT,
        value REAL,
        FOREIGN KEY (zip_code) REFERENCES Locations(zip_code)
    )
    """)
    
    conn.commit()

def get_coordinates(zip_code, conn):
    """Retrieve latitude and longitude for a given ZIP code."""
    cursor = conn.cursor()
    cursor.execute("SELECT lat, long FROM Locations WHERE zip_code = ?", (zip_code,))
    result = cursor.fetchone()
    return result if result else None

def insert_user_data(zip_code, category, value, conn):
    """Insert a new entry into UserData for custom categories and values."""
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO UserData (zip_code, category, value)
    VALUES (?, ?, ?)
    """, (zip_code, category, value))
    
    conn.commit()

# Initialize database and create tables if needed
if __name__ == "__main__":
    conn = connect_db(db_path)
    create_tables(conn)
    conn.close()
