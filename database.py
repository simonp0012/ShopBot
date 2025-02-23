import sqlite3  # Importing sqlite3 module to interact with SQLite databases

DB_FILE = "users.db"  # Defining the database file name

def create_tables():
    # Connecting to the SQLite database (or creating it if it doesn't exist)
    conn = sqlite3.connect(DB_FILE)
    # Creating a cursor object to execute SQL commands
    cursor = conn.cursor()

    # Executing an SQL command to create the 'users' table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  # Unique ID for each user, auto-incremented
        username TEXT UNIQUE NOT NULL,  # Username, must be unique and not null
        password TEXT NOT NULL,  # Password, must not be null
        email TEXT DEFAULT '',  # Email, default is an empty string
        phone TEXT DEFAULT ''  # Phone number, default is an empty string
    )
    """)

    # Committing the changes to the database
    conn.commit()
    # Closing the database connection
    conn.close()