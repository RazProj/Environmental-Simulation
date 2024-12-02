def calc_temp_avg(map_gen, cell):
    """ Compute the average temperature of a cell's neighbors. """
    neighbors = map_gen.get_neighbors(cell.x, cell.y)
    if not neighbors:
        raise ValueError("Valid input")
    total_temp = sum(neighbor.get_temp() for neighbor in neighbors)
    return total_temp / len(neighbors) 

def calc_pollution_avg(map_gen, cell):
    """Calculate the average pollution level of neighboring cells."""
    neighbors = map_gen.get_neighbors(cell.x, cell.y)
    if not neighbors:
        return 0  # Avoid division by zero
    total_pollution = sum(neighbor.get_pollution() for neighbor in neighbors)
    return total_pollution / len(neighbors) 

def calc_temp_w(map_gen, cell):
    """Calculate the wind effect on temperature for a cell."""
    neighbors = map_gen.get_neighbors(cell.x, cell.y)
    wind_neighbors = filter_neighbors_by_wind(cell, neighbors)
    wind_effect = 0
    for neighbor in wind_neighbors:
        wind_effect += cell.get_wind_speed() * (abs(neighbor.get_temp() - cell.get_temp()))
    return wind_effect

def calc_pollution_w(map_gen, cell):
    """Calculate the wind effect on pollution for a cell."""
    neighbors = map_gen.get_neighbors(cell.x, cell.y)
    wind_neighbors = filter_neighbors_by_wind(cell, neighbors)
    wind_effect = 0
    for neighbor in wind_neighbors:
        wind_effect += cell.get_wind_speed() * (neighbor.get_pollution() - cell.get_pollution())
    return wind_effect

def filter_neighbors_by_wind(cell, neighbors):
    """ Filter neighbors to include only those whose wind blows towards the given cell. """
    wind_affected_neighbors = []
    for neighbor in neighbors:
        wind_direction = neighbor.get_wind_direction()
        if wind_direction == 'S' and neighbor.x == cell.x and neighbor.y > cell.y:
            wind_affected_neighbors.append(neighbor)
        elif wind_direction == 'N' and neighbor.x == cell.x and neighbor.y < cell.y:
            wind_affected_neighbors.append(neighbor)
        elif wind_direction == 'E' and neighbor.y == cell.y and neighbor.x < cell.x:
            wind_affected_neighbors.append(neighbor)
        elif wind_direction == 'W' and neighbor.y == cell.y and neighbor.x > cell.x:
            wind_affected_neighbors.append(neighbor)
    return wind_affected_neighbors

def calc_temp_difference(cell, neighbors):
    """Calculate the absolute temperature differences between a cell and its neighbors."""
    return [abs(cell.get_temp() - neighbor.get_temp()) for neighbor in neighbors]

def increase_get_pollution(cell):
    """ global pollution factor growth"""
    if cell.element == 'city':
        # Get the current generation rate
        current_gen_pollution = cell.get_gen_pollution()
        # Increase pollution generation for cities
        cell.set_gen_pollution(current_gen_pollution + 0.1)

def calc_global_avg_temp(map):
    """ Calculate the global average temperature for the entire map. """
    total_temp = 0
    cell_count = 0

    for row in map:
        for cell in row:
            total_temp += cell.get_temp()
            cell_count += 1

    return total_temp / cell_count if cell_count > 0 else 0

def calc_global_avg_pollution(map):
    """ Calculate the global average pollution for the entire map. """
    total_pollution = 0
    cell_count = 0

    for row in map:
        for cell in row:
            total_pollution += cell.get_pollution()
            cell_count += 1

    return total_pollution / cell_count if cell_count > 0 else 0


