import datetime
# creating the Truck class
class Truck:
    def __init__(self, truck_id, capacity=16, speed=18):
        self.truck_id = truck_id
        self.capacity = capacity
        self.speed = speed
        self.packages = []
        self.route = []
        self.total_distance = 0.0
        self.total_time = 0.0
        self.current_location = 0
        self.start_time = datetime.timedelta(hours=8)
        self.current_time = self.start_time

    def load_package(self, package):
        if len(self.packages) < self.capacity:
            self.packages.append(package)
            return True
        return False

    def load_packages_by_ids(self, package_ids, package_hash_table):
        for pid in package_ids:
            if pid in package_hash_table:
                loaded = self.load_package(package_hash_table[pid])
                if not loaded:
                    print(f"Truck {self.truck_id} is full. Can't load package {pid}.")
                    break
            else:
                print(f"Package ID {pid} not found.")

    def deliver_packages(self, address_to_index, distance_matrix, tsp_nearest_neighbor, return_to_hub=True):
        print(f"Starting delivery for Truck {self.truck_id}...")
        self.current_location = self.route[0]
        self.current_time = self.start_time

        for pkg in self.packages:
            pkg.departure_time = self.start_time
            pkg.status = "En Route"

        pending_packages = self.packages.copy()
        visited_stops = set([self.current_location])

        while pending_packages:
            reroute_needed = False
            for pkg in pending_packages:
                old_address = pkg.address
                pkg.update_address_if_time(self.current_time)
                if old_address != pkg.address:
                    reroute_needed = True
                    print(f"Package {pkg.ID} address updated to {pkg.address} at {self.current_time}")

            if reroute_needed:
                delivery_indices = set([self.current_location])
                for pkg in pending_packages:
                    delivery_indices.add(address_to_index[pkg.address])
                self.route, _, _ = tsp_nearest_neighbor(self.current_location, distance_matrix, list(delivery_indices))
                print(f"Rerouted at {self.current_time}. New route: {self.route}")

            next_stop = None
            for stop in self.route:
                if stop not in visited_stops:
                    next_stop = stop
                    break

            if next_stop is None:
                break

            distance = float(distance_matrix[self.current_location][next_stop])
            travel_time = datetime.timedelta(hours=distance / self.speed)
            self.current_time += travel_time
            self.total_distance += distance
            self.total_time = (self.current_time - self.start_time).total_seconds() / 3600
            self.current_location = next_stop
            visited_stops.add(next_stop)

            delivered = []
            for pkg in pending_packages:
                if not pkg.address:
                    continue
                if address_to_index[pkg.address] == next_stop:
                    pkg.status = "Delivered"
                    pkg.delivery_time = self.current_time
                    delivered.append(pkg)

            for pkg in delivered:
                pending_packages.remove(pkg)
                print(f"Delivered package {pkg.ID} at address: {pkg.address} at {self.current_time}")

            print(
                f"Arrived at location {next_stop}, distance traveled: {self.total_distance:.2f} miles, total time: {self.total_time:.2f} hours")

        print(f"Delivery complete for Truck {self.truck_id} at {self.current_time}")

        if return_to_hub and self.current_location != 0:
            distance_back = float(distance_matrix[self.current_location][0])
            travel_time = datetime.timedelta(hours=distance_back / self.speed)
            self.current_time += travel_time
            self.total_distance += distance_back
            self.total_time = (self.current_time - self.start_time).total_seconds() / 3600
            self.current_location = 0
            print(
                f"Returned to hub, distance traveled: {self.total_distance:.2f} miles, total time: {self.total_time:.2f} hours")

    def clear(self):
        self.packages = []
        self.route = []
        self.total_distance = 0.0
        self.total_time = 0.0
        self.current_location = 0
        self.start_time = datetime.timedelta(hours=8)
        self.current_time = self.start_time
