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
        CREATE TABLE IF NOT EXISTS parking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id INTEGER NOT NULL,
            check_in_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            check_out_time DATETIME,
            status TEXT NOT NULL DEFAULT 'PARKED',

            FOREIGN KEY (vehicle_id)
            REFERENCES vehicles(id)
        )    
    """)

    #closing the connection
    conn.commit()
    conn.close()

def add_vehicles(plate_number):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO vehicles (plate_number) VALUES (?)
    """,(plate_number,))
    # passing plate number as a tuple of size 1 

    conn.commit()
    vehicle_id = cursor.lastrowid
    conn.close()
    return vehicle_id


def get_vehicle(plate_number):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM vehicles where plate_number = ?
    """,(plate_number,))

    vehicle = cursor.fetchone()
    conn.close()
    return vehicle



def create_parking_entry(vehicle_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO parking (vehicle_id)
        VALUES (?)
    """, (vehicle_id,))

    conn.commit()

    parking_id = cursor.lastrowid

    conn.close()

    return parking_id
    
def check_in(plate_number):
    conn = get_conn()
    cursor = conn.cursor()

    # Check whether vehicle already exsists or not 
    vehicle = get_vehicle(plate_number)
    # If vehicle does not exsist add or else get the vehicle if 
    if vehicle is None:
        vehicle_id = add_vehicles(plate_number)
    else:
        vehicle_id = vehicle["id"]

    # Now check with the vehicle_id that is it already parked

    cursor.execute("""
        SELECT * FROM parking WHERE  vehicle_id = ? AND status = 'PARKED'
    """)

    active_parking = cursor.fetchone()
    conn.close()

    if active_parking:
        return {
            "success": False,
            "message": "Vehicle is already checked in.",
            "vehicle_id": vehicle_id,
            "parking_id": active_parking["id"]
        }
    

    parking_id = create_parking_entry(vehicle_id)
    return {
        "success": True,
        "message": "Vehicle checked in successfully.",
        "vehicle_id": vehicle_id,
        "parking_id": parking_id
    }
