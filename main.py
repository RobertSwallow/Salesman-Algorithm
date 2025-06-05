import csv
from datetime import timedelta

from hash_table import HashMap
from loader import load_truck
from package import Package
from address_distance_loader import load_address_data, load_distance_data, get_distance
from tsp import tsp_nearest_neighbor
from truck import Truck

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

def get_distance(address1, address2, address_to_index, distance_matrix):
    i = address_to_index[address1]
    j = address_to_index[address2]
    return distance_matrix[i][j]




truck1 = Truck(truck_id=1)
truck2 = Truck(truck_id=2)
truck3 = Truck(truck_id=3)

package_hash_table = HashMap()
load_package_data("Resources/packages.csv", package_hash_table)


load1 = [13, 14, 15, 16, 19, 20, 34, 21, 12, 13, 39, 27, 35]
load3 = [6, 17, 31, 32, 4, 40, 28, 1, 2, 33, 7, 29, 10]
load2 = [3, 5, 8, 9, 11, 18, 22, 23, 24, 25, 26, 30, 36, 37, 38]


package_9 = package_hash_table.lookup(9)
package_9.address = ""
package_9.delayed_address_update_time = timedelta(hours=10, minutes=20)
package_9.delayed_address = "410 S State St"

truck1, delivery_indices1 = load_truck(package_hash_table, address_to_index, load1, truck1)
truck2, delivery_indices2 = load_truck(package_hash_table, address_to_index, load2, truck2)
truck3, delivery_indices3 = load_truck(package_hash_table, address_to_index, load3, truck3)

route1, dist1, time1 = tsp_nearest_neighbor(0, distance_matrix, delivery_indices1)
truck1.route = route1
truck1.total_distance = 0

route2, dist2, time2 = tsp_nearest_neighbor(0, distance_matrix, delivery_indices2)
truck2.route = route2
truck2.total_distance = 0

route3, dist3, time3 = tsp_nearest_neighbor(0, distance_matrix, delivery_indices3)
truck3.route = route3
truck3.total_distance = 0


truck1.start_time = timedelta(hours=8)
truck2.start_time = timedelta(hours=10, minutes=21)
truck3.start_time = timedelta(hours=9, minutes=30)


truck1.deliver_packages(address_to_index, distance_matrix, tsp_nearest_neighbor, return_to_hub=True)
truck2.deliver_packages(address_to_index, distance_matrix, tsp_nearest_neighbor, return_to_hub=False)
truck3.deliver_packages(address_to_index, distance_matrix, tsp_nearest_neighbor, return_to_hub=False)


ids = load1 + load2 + load3
ids.sort()
for pid in ids:
    package = package_hash_table.lookup(pid)
    if package:
        print(f"Package {package.ID} status: {package.status}")

print(f"Truck {truck1.truck_id} route: {truck1.route}")
print(f"Total distance: {truck1.total_distance:.2f} miles")
print(f"Total time: {truck1.total_time:.2f} hours")

print(f"Truck {truck2.truck_id} route: {truck2.route}")
print(f"Total distance: {truck2.total_distance:.2f} miles")
print(f"Total time: {truck2.total_time:.2f} hours")

print(f"Truck {truck3.truck_id} route: {truck3.route}")
print(f"Total distance: {truck3.total_distance:.2f} miles")
print(f"Total time: {truck3.total_time:.2f} hours")

total_miles = truck1.total_distance + truck2.total_distance + truck3.total_distance



print(f"total miles for all trips:  {total_miles:.2f} miles")