import csv

# Loads distances into matrix for future use
def load_address_data(filename):
    address_to_index = {}
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            index = int(row[0])
            address = row[2]
            address_to_index[address] = index
    return address_to_index

def load_distance_data(filename):
    distance_matrix = []
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            distance_row = [float(cell) if cell else 0.0 for cell in row]
            distance_matrix.append(distance_row)
    return distance_matrix

def get_distance(matrix, index1, index2):
    distance = matrix[index1][index2]
    if distance == '':
        distance = matrix[index2][index1]
    return float(distance)
