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
    get_parking_amount
)


# Create Database Tables


# create_tables()

# print("\n==========================")
# print("DATABASE TEST")
# print("==========================\n")


# # 1. Add Vehicle


# plate = "MP09AA1234"

# vehicle = get_vehicle(plate)

# if vehicle is None:

#     vehicle_id = add_vehicles(plate)

#     print("Vehicle created successfully.")
#     print("Vehicle ID:", vehicle_id)

# else:

#     vehicle_id = vehicle["id"]

#     print("Vehicle already exists.")
#     print("Vehicle ID:", vehicle_id)



# # 2. Check-In


# print("\n--- CHECK-IN ---")

# result = check_in(plate)

# print(result)



# # 3. Try Check-In Again


# print("\n--- SECOND CHECK-IN ---")

# result = check_in(plate)

# print(result)



# # 4. Check-Out


# print("\n--- CHECK-OUT ---")

# result = check_out(plate)

# print(result)


# # 5. Try Check-Out Again


# print("\n--- SECOND CHECK-OUT ---")

# result = check_out(plate)

# print(result)


# # ==========================
# # Display Vehicles
# # ==========================

# print("\n--- VEHICLES DATABASE ---")

# vehicles = get_all_vehicles()

# for vehicle in vehicles:

#     print(
#         dict(vehicle)
#     )


# # ==========================
# # Display Parking Database
# # ==========================

# print("\n--- PARKING DATABASE ---")

# parking_records = get_all_parking_records()

# for record in parking_records:

#     print(
#         dict(record)
#     )

val = get_parking_amount(1)
print(val["TIME"])
print(val["AMOUNT"],"/-")


# ==========================
# DATABASE TEST
# ==========================

# Vehicle created successfully.
# Vehicle ID: 1

# --- CHECK-IN ---
# {'success': True, 'message': 'Vehicle checked in successfully.', 'vehicle_id': 1, 'parking_id': 1}

# --- SECOND CHECK-IN ---
# {'success': False, 'message': 'Vehicle is already checked in.', 'vehicle_id': 1, 'parking_id': 1}

# --- CHECK-OUT ---
# {'success': True, 'message': 'Vehicle checked out successfully.', 'vehicle_id': 1, 'parking_id': 1}

# --- SECOND CHECK-OUT ---
# {'success': False, 'message': 'No matching parking record found. Vehicle is not currently parked.'}

# --- VEHICLES DATABASE ---
# {'id': 1, 'plate_number': 'MP09AA1234', 'vehicle_type': 'Car'}

# --- PARKING DATABASE ---
# {'id': 1, 'vehicle_id': 1, 'check_in_time': '2026-08-08 07:57:47', 'check_out_time': '2026-08-08 07:57:47', 'status': 'COMPLETED'}