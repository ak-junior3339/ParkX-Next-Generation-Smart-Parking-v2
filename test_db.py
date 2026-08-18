from database import (
    get_conn,
    create_tables,
    add_vehicles,
    get_vehicle,
    create_parking_entry,
    check_in,
    check_out,
    get_all_vehicles,
    get_all_parking_records,
    get_parking_amount,
    payment_status
)
from database import *

# 1. Create tables
create_tables()

# 2. Add vehicles
vehicle1 = add_vehicles("MP04AB1234")
vehicle2 = add_vehicles("MP09CD5678")

print("Vehicle 1 ID:", vehicle1)
print("Vehicle 2 ID:", vehicle2)

# 3. Get vehicle
vehicle = get_vehicle("MP04AB1234")
print("Vehicle:", dict(vehicle))

# 4. Check in
result = check_in("MP04AB1234")
print("Check-in:", result)

# 5. Check another vehicle in
result = check_in("MP09CD5678")
print("Check-in:", result)



# 7. Display all vehicles
vehicles = get_all_vehicles()

print("\nAll Vehicles:")
for vehicle in vehicles:
    print(dict(vehicle))

# 8. Display parking records
parking = get_all_parking_records()

print("\nParking Records:")
for record in parking:
    print(dict(record))
    
# Check out vehicle
result = check_out("MP04AB1234")

print("\nCheck-out:")
print(result)

# Get parking ID
park_id = result["parking_id"]

# Mark payment as done
payment = payment_status(park_id)

print("\nPayment:")
print(payment)

# Check database
parking = get_all_parking_records()

print("\nUpdated Parking Records:")
for record in parking:
    print(dict(record))