def tsp_nearest_neighbor(start_index, distance_matrix, delivery_indices, speed_mph=18):
    route = [start_index]
    unvisited = set(delivery_indices)
    unvisited.discard(start_index)
    current = start_index
    total_distance = 0.0

    while unvisited:
        next_stop = min(unvisited, key=lambda i: distance_matrix[current][i])
        distance = distance_matrix[current][next_stop]
        total_distance += distance
        route.append(next_stop)
        unvisited.remove(next_stop)
        current = next_stop

    return_distance = distance_matrix[current][start_index]
    total_distance += return_distance
    route.append(start_index)

    total_time_hours = total_distance / speed_mph

    return route, round(total_distance, 2), round(total_time_hours, 2)
