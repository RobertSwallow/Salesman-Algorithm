# Student ID: 011980491

import csv
from datetime import timedelta
from hash_table import HashMap
from loader import load_truck
from package import Package
from address_distance_loader import load_address_data, load_distance_data
from tsp import tsp_nearest_neighbor
from truck import Truck

# Created Matrix for Packages
def load_package_data(filename, package_hash_table):
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            package_id = row[0]
            address = row[1]
            city = row[2]
            state = row[3]
            zip_code = row[4]
            deadline = row[5]
            weight = row[6]
            special_notes = row[7]

            package = Package(package_id, address, city, state, zip_code, deadline, weight, special_notes)
            package_hash_table.insert(int(package_id), package)


address_to_index = load_address_data("Resources/addresses.csv")
distance_matrix = load_distance_data("Resources/distances.csv")


# creates a function for calling on the distance matrix
def get_distance(address1, address2, address_to_index, distance_matrix):
    i = address_to_index[address1]
    j = address_to_index[address2]
    return distance_matrix[i][j]



# creates different trucks and calls on the package loader to get ready for loading trucks
truck1 = Truck(truck_id=1)
truck2 = Truck(truck_id=2)
truck3 = Truck(truck_id=3)

package_hash_table = HashMap()
load_package_data("Resources/packages.csv", package_hash_table)

# loads decided with much work to find a good route for a reasonable time and the shortest distance
load1 = [13, 14, 15, 16, 19, 20, 34, 21, 12, 39, 27, 35]
load2 = [3, 5, 8, 9, 11, 18, 22, 23, 24, 25, 26, 30, 36, 37, 38]
load3 = [6, 17, 31, 32, 4, 40, 28, 1, 2, 33, 7, 29, 10]

# Create the address change for package 9 at the correct time
package_9 = package_hash_table.lookup(9)
package_9.address = ""
package_9.delayed_address_update_time = timedelta(hours=10, minutes=20)
package_9.delayed_address = "410 S State St"


# getting the loads ready to be put in the trucks
truck1, delivery_indices1 = load_truck(package_hash_table, address_to_index, load1, truck1)
truck2, delivery_indices2 = load_truck(package_hash_table, address_to_index, load2, truck2)
truck3, delivery_indices3 = load_truck(package_hash_table, address_to_index, load3, truck3)

# creating routes based on TSP nearest neighbor
route1, dist1, time1 = tsp_nearest_neighbor(0, distance_matrix, delivery_indices1)
truck1.route = route1
truck1.total_distance = 0

route2, dist2, time2 = tsp_nearest_neighbor(0, distance_matrix, delivery_indices2)
truck2.route = route2
truck2.total_distance = 0

route3, dist3, time3 = tsp_nearest_neighbor(0, distance_matrix, delivery_indices3)
truck3.route = route3
truck3.total_distance = 0

# setting truck start times
truck1.start_time = timedelta(hours=8)
truck2.start_time = timedelta(hours=9, minutes=30)
truck3.start_time = timedelta(hours=9, minutes=6)

# deliver the packages and making sure that the first driver makes it back to the hub while the other two deliveries don't need to return
truck1.deliver_packages(address_to_index, distance_matrix, tsp_nearest_neighbor, return_to_hub=True)
truck2.deliver_packages(address_to_index, distance_matrix, tsp_nearest_neighbor, return_to_hub=False)
truck3.deliver_packages(address_to_index, distance_matrix, tsp_nearest_neighbor, return_to_hub=False)

# gathering all package ids and sorting them for future use
ids = load1 + load2 + load3
ids.sort()

# updating the status based on the current time
def update_all_package_statuses(packages, current_time):
    for pkg in packages:
        pkg.update_address_if_time(current_time)
        pkg.update_status(current_time)

# calculating the total miles
total_miles = truck1.total_distance + truck2.total_distance + truck3.total_distance

# Calculating latest delivery time
def get_last_delivery_time(truck):
    return max(pkg.delivery_time for pkg in truck.packages if pkg.delivery_time)

last_times = [
    get_last_delivery_time(truck1),
    get_last_delivery_time(truck2),
    get_last_delivery_time(truck3)
]
final_time = max(last_times)



print()
print()
print(f"Total miles for all trips:  {total_miles:.2f} miles")
print(f"Time of last delivery:   {final_time}")

# making the logic for printing out where all packages are based on time and printing it
def display_all_package_statuses(packages, current_time):
    print(f"\nStatus of all packages at {str(current_time)}:\n")
    update_all_package_statuses(packages, current_time)
    print("\nDelivered Packages:")
    for pid in ids:
        package = package_hash_table.lookup(pid)
        if package and package.status.startswith("Delivered"):
                print(f"Package {package.ID:2} status: {package.status}")

    print("\nPackages still at hub:")
    at_hub_packages = [pkg for pkg in packages if pkg.status == "At Hub"]
    if at_hub_packages:
        for pkg in at_hub_packages:
            print(f"Package {pkg.ID:2}")
    else:
        print("None")


    truck1_en_route = [pkg for pkg in packages if pkg.status.startswith("En") and pkg.truck == "Truck 1"]
    if truck1_en_route:
        print("\nTruck 1 Packages En Route:")
        for pkg in truck1_en_route:
            print(f"Package {pkg.ID:2}")

    truck2_en_route = [pkg for pkg in packages if pkg.status.startswith("En") and pkg.truck == "Truck 2"]
    if truck2_en_route:
        print("\nTruck 2 Packages En Route:")
        for pkg in truck2_en_route:
            print(f"Package {pkg.ID:2}")

    truck3_en_route = [pkg for pkg in packages if pkg.status.startswith("En") and pkg.truck == "Truck 3"]
    if truck3_en_route:
        print("\nTruck 3 Packages En Route:")
        for pkg in truck3_en_route:
            print(f"Package {pkg.ID:2}")

def time_change(time_str):
    hour, minute = map(int, time_str.split(":"))
    return timedelta(hours=hour, minutes=minute)

def get_all_packages(hash_table):
    all_packages = []
    for bucket in hash_table.table:
        if bucket is not None:
            for key, package in bucket:
                all_packages.append(package)
    return all_packages

def lookup_package(package_id, current_time):
    package = package_hash_table.lookup(package_id)
    if not package:
        print(f"No package found with ID {package_id}")
        return

    update_all_package_statuses([package], current_time)

    print(f"\nPackage {package.ID} Information at {current_time}:")
    print(f"Address: {package.address}")
    print(f"Deadline: {package.deadline}")
    print(f"City: {package.city}")
    print(f"ZIP Code: {package.zip_code}")
    print(f"Weight: {package.weight}")
    print(f"Status: {package.status}")



print()
print()

if __name__ == "__main__":
    print("1. View status of all packages at a given time")
    print("2. View status of a specific package at a given time")
    print("3. View total mileage of all trucks")
    choice = input("Choose an option (1–3): ")

    if choice == "1":
        user_input = input("Enter time (HH:MM): ")
        current_time = time_change(user_input)
        all_packages = get_all_packages(package_hash_table)
        display_all_package_statuses(all_packages, current_time)

    elif choice == "2":
        package_id = int(input("Enter package ID: "))
        user_input = input("Enter time (HH:MM): ")
        current_time = time_change(user_input)
        lookup_package(package_id, current_time)
        package = package_hash_table.lookup(package_id)
        update_all_package_statuses([package], current_time)
        if package:
            print(f"Package {package.ID} status at {current_time}: {package.status}")

    elif choice == "3":
        total_miles = truck1.total_distance + truck2.total_distance + truck3.total_distance
        print(f"Truck 1: {truck1.total_distance}")
        print(f"Truck 2: {truck2.total_distance}")
        print(f"Truck 3: {truck3.total_distance}")
        print(f"Total miles for all trips: {total_miles:.2f} miles")
