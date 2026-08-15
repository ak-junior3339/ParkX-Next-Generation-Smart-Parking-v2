import sqlite3
import math
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
            Ttime REAL,
            Tamount INTEGER,

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

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO parking (vehicle_id)
        VALUES (?)
    """, (vehicle_id,))

    conn.commit()

    parking_id = cursor.lastrowid

    conn.close()

    return parking_id
    

# Function for checking in the vehicle     
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
    """,(vehicle_id,))

    active_parking = cursor.fetchone()
    conn.close()

    if active_parking:
        return {
            "success": False,
            "message": "Vehicle is already checked in.",
            "vehicle_id": vehicle_id,
            "parking_id": active_parking["id"]
        }
    
    # Creating a parking record if not already exsists
    parking_id = create_parking_entry(vehicle_id)
    return {
        "success": True,
        "message": "Vehicle check in successfull",
        "vehicle_id": vehicle_id,
        "parking_id": parking_id,
        "plate" : plate_number
    }

# Function for checking out the vehicle
def check_out(plate_number):
    conn = get_conn()
    cursor = conn.cursor()

    # First job is to check wheteher vehicle exsists or not
    vehicle = get_vehicle(plate_number)
    if vehicle is None:
        conn.close()
        return {
            "success": False,
            "message": "Vehicle does not exist."
        }
    vehicle_id = vehicle["id"]

    cursor.execute("""
        SELECT * FROM parking WHERE vehicle_id = ? AND status = 'PARKED'
    """,(vehicle_id,))

    parking_record = cursor.fetchone()

    if parking_record is None :
        conn.close()
        return {
            "success": False,
            "message": "No matching parking record found. Vehicle is not currently parked."
        }
    
    cursor.execute("""
        UPDATE parking SET check_out_time = CURRENT_TIMESTAMP,status = 'COMPLETED' where id = ?
    """,(parking_record["id"],))
    conn.commit()
    conn.close()
    final_cost = get_parking_amount(parking_record["id"])

    return {
        "success": True,
        "message": "Vehicle check out successfull ",
        "vehicle_id": vehicle_id,
        "parking_id": parking_record["id"],
        "pNumber" : plate_number,
        "time" : final_cost["TIME"] ,
        "amount":final_cost["AMOUNT"]
    }

def get_parking_amount(park_id):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT (JULIANDAY(check_out_time) - JULIANDAY(check_in_time))*24 FROM parking WHERE 
        id = ?
    """,(park_id,))
    PRICE_PER_HOUR = 20
    time  = cursor.fetchone()[0]
    amount = math.ceil(time) * PRICE_PER_HOUR

    cursor.execute("""
        UPDATE parking SET Ttime = ? , Tamount = ? WHERE id = ?
    """,(time,amount,park_id))
    conn.commit()
    conn.close()
    return {
        "TIME":f"{time:.3f}",
        "AMOUNT":amount
    }

# Getting all vehicle information 
def get_all_vehicles():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM vehicles
    """)

    vehicles = cursor.fetchall()
    conn.close()

    return vehicles


# Getting all parking records 
def get_all_parking_records():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM parking
    """)
    parking_record = cursor.fetchall()
    conn.close()
    return parking_record

def get_all_stats():
    conn = get_conn()
    cursor = conn.cursor()
    ## Query to get total vehicles 
    cursor.execute("""
        SELECT COUNT(*) FROM vehicles
    """)
    total_vehicles = cursor.fetchone()[0]

    ## Query for Currently parked
    cursor.execute("""
        SELECT COUNT(*) FROM parking WHERE status = 'PARKED'
    """)
    curr_park = cursor.fetchone()[0]

    ## Available Parking 
    PARKING_CAPACITY = 100
    available = PARKING_CAPACITY - curr_park

    # Today's check-ins
    cursor.execute("""
        SELECT COUNT(*)
        FROM parking
        WHERE DATE(check_in_time) = DATE('now')
    """)
    today_checkins = cursor.fetchone()[0]

    conn.close()

    return {
        "total_vehicles": total_vehicles,
        "currently_parked": curr_park,
        "available": available,
        "today_checkins": today_checkins
    }
## Function for fetching the searched car in admin section
def get_admin_search(plate):
    conn = get_conn()
    cursor = conn.cursor()
    # it cannot happen using simple queries so we use join 
    cursor.execute("""
        SELECT
            parking.id,
            vehicles.plate_number,
            vehicles.vehicle_type,
            parking.check_in_time,
            parking.check_out_time,
            parking.status
        FROM parking
        JOIN vehicles
            ON parking.vehicle_id = vehicles.id
        WHERE vehicles.plate_number = ?
    """, (plate,))

    rows = cursor.fetchall()

    conn.close()

    return rows

