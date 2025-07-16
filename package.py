# creating the package class
class Package:
    def __init__(self, package_id, address, city, state, zip_code, deadline, weight, special_notes):
        self.ID = int(package_id)
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.special_notes = special_notes
        self.status = "At Hub"
        self.delivery_time = None
        self.departure_time = None
        self.delayed_address_update_time = None
        self.delayed_address = None
        self.truck = None

    # creating time logic
    def update_address_if_time(self, current_time):
        if self.delayed_address_update_time and current_time >= self.delayed_address_update_time:
            self.address = self.delayed_address
            self.delayed_address_update_time = None

    # creating status update logic
    def update_status(self, current_time):
        if self.delivery_time is not None and current_time >= self.delivery_time:
            self.status = f"Delivered at {self.delivery_time}"
        elif self.departure_time <= current_time < self.delivery_time:
            self.status = "En route"
        else:
            self.status = "At Hub"
    def update_all_package_statuses(packages, current_time):
        for pkg in packages:
            pkg.update_status(current_time)