# creating the loader for the packages

def load_truck(package_hash_table, address_to_index, package_ids, truck):
    for package_id in package_ids:
        package = package_hash_table.lookup(package_id)
        if package:
            package.truck =f"Truck {truck.truck_id}"
            truck.load_package(package)

    delivery_indices = set()
    delivery_indices.add(0)

    for pkg in truck.packages:
        if pkg.address:
            delivery_indices.add(address_to_index[pkg.address])

    return truck, list(delivery_indices)
