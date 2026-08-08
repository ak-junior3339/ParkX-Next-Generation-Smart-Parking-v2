import sqlite3

DATABASE = "Parking.db"

def get_conn():
    conn = sqlite3.connect(DATABASE)
    # This allows you to access database columns by name (like a dictionary) in addition to index positions
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    # Creating a Connection with sqlite3
    conn = get_conn()
    cursor = conn.cursor()

    # Creating tables
    # Vehicle Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS  vehicles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plate_number TEXT UNIQUE NOT NULL,
        vehicle_type TEXT NOT NULL DEFAULT 'Car'
        )
    """)

    # Now creating Parking table 
    cursor.execute("""
        CREATE TABLE IF NOT EXSISTS parking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id INTEGER NOT NULL,
            check_in_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            check_out_time DATETIME,
            status TEXT NOT NULL DEFAULT 'PARKED',

            FOREIGN KEY (vehicle_id)
            REFERENCES vehicles(id)
        )    
    """)
    conn.commit()
    conn.close()

