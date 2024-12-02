import math
from calculation_utils import calc_temp_avg, calc_pollution_avg, calc_pollution_w, calc_temp_difference, calc_temp_w, calc_global_avg_temp, calc_global_avg_pollution


"""
Weights for controlling the impact of each parameter in the cell according to it`s element:
- alpha: The impact of the current temperature of the cell
- beta: The impact of the average neighbors temperatures
- gamma: The impact of the pollution 
- delta: The impact of the wind    
"""
TEMP_WEIGHTS_FOR_GLACIERS = {'alpha': 0.05, 'beta': 1.5, 'gamma': 0.6, 'delta': 0.00001} 
TEMP_WEIGHTS_FOR_CITY = {'alpha': 0.4, 'beta': 0.01, 'gamma': 0.8, 'delta': 0.00001}
TEMP_WEIGHTS_FOR_ELSE = {'alpha': 0.6, 'beta': 0.9, 'gamma': 0.9, 'delta': 0.00001}

POLLUTION_WEIGHTS = {
    'alpha': 0.2,  # Weight for the cell's own pollution
    'beta': 0.1  # Weight for the pollution levels of neighboring cells
}  # Adjusted to reduce instability and ensure steadier growth.


WIND_MODIFIER_MAP = {
    'sea': 1.2,   # Strong winds over water
    'forest': 0.5,  # Reduced wind in forests
    'city': 0.8,  # Wind resistance in urban areas
    'glacier': 1.0,  # Moderate winds over glaciers
    'land': 1.0    # Neutral default
}

SCALING_FACTOR = 0.02  # Controls the overall impact of wind speed on temperature and pollution.

CLOUD_EFFECTS = {'cloud': 0, 'rain': -0.0005, '': 0} # Rain reduces pollution.

DAMPENING_FACTOR = {
    'temp_dampening': 0.05,  # Controls the smoothness of temperature changes.
    'pollution_dampening': 0.002  # Moderates abrupt changes in pollution levels.
}  

def calc_temp(map, map_gen, cell):
    """
    Calculate the updated temperature of a cell based on various factors:
    
    Factors:
    - Cell's current temperature (self-influence).
    - Average temperature of neighboring cells (environmental influence).
    - Pollution levels (pollution contributes to temperature changes).
    - Wind effects (temperature differences due to wind).
    - Cloud presence (cooling effects of clouds or rain).

    Cloud effects:
    - None: No impact on temperature.
    - 'cloud': Negligible cooling.
    - 'rain': Slight cooling effect.

    BASELINE_TEMP_GROWTH is a constant growth factor to simulate overall temperature rise.

    Returns:
    - new_temp (float): The updated temperature after applying all adjustments.
    """

    temperature = cell.get_temp()
    temp_avg = calc_temp_avg(map_gen, cell)
    pollution = cell.get_pollution()
    wind_temp = calc_temp_w(map_gen, cell)
    cloud = cell.get_cloud()
    # Define cloud effects: cooling impact on temperature
    cloud_effect = CLOUD_EFFECTS.get(cloud, 0) # Use default of 0 if cloud is not in CLOUD_EFFECTS
    global_average_temperature = calc_global_avg_temp(map)
    global_average_pollution = calc_global_avg_pollution(map)
    BASELINE_TEMP_GROWTH = abs(temperature -  global_average_temperature) * 0.1
    # Combine all factors to calculate the raw new temperature using "Weighted Linear Combination with Dampening"
    if cell.get_element() == 'glacier':
        raw_new_temp = (TEMP_WEIGHTS_FOR_GLACIERS['alpha'] * temperature +  
                        TEMP_WEIGHTS_FOR_GLACIERS['beta'] * temp_avg +      
                        TEMP_WEIGHTS_FOR_GLACIERS['gamma'] * pollution +    
                        TEMP_WEIGHTS_FOR_GLACIERS['delta'] * wind_temp + 
                        BASELINE_TEMP_GROWTH +
                        cloud_effect)                         
    elif cell.get_element() == 'city':
        raw_new_temp = (TEMP_WEIGHTS_FOR_CITY['alpha'] * temperature +  
                        TEMP_WEIGHTS_FOR_CITY['beta'] * temp_avg +      
                        TEMP_WEIGHTS_FOR_CITY['gamma'] * pollution +    
                        TEMP_WEIGHTS_FOR_CITY['delta'] * wind_temp + 
                        BASELINE_TEMP_GROWTH +
                        cloud_effect)       
    else:
        raw_new_temp = (TEMP_WEIGHTS_FOR_ELSE['alpha'] * temperature +  
                        TEMP_WEIGHTS_FOR_ELSE['beta'] * temp_avg +      
                        TEMP_WEIGHTS_FOR_ELSE['gamma'] * pollution +    
                        TEMP_WEIGHTS_FOR_ELSE['delta'] * wind_temp + 
                        BASELINE_TEMP_GROWTH +
                        cloud_effect)       


    # Apply a dampening factor to prevent drastic changes in temperature
    new_temp = temperature + DAMPENING_FACTOR['temp_dampening'] * (abs(raw_new_temp - temperature) * 0.1 * global_average_pollution )
    return max(new_temp, temperature) 


def calc_pollution(map, map_gen, cell):
    """
    Calculate the updated pollution level of a cell considering:
    - Current pollution levels
    - Neighboring pollution levels
    - Pollution generated and absorbed by the cell
    - Effects of wind and rain

    Special considerations:
    - Rain reduces pollution slightly.
    - Ensures non-negative pollution levels.

    Returns:
    - new_pollution (float): Updated pollution value for the cell.
    """
    pollution = cell.get_pollution()
    pollution_avg = calc_pollution_avg(map_gen, cell)
    gen_pollution = cell.get_gen_pollution()
    absorb_pollution = cell.get_absorb_pollution()
    wind_pollution = calc_pollution_w(map_gen, cell)
    cloud = cell.attributes_val.get('clouds', None)
    global_average_pollution = calc_global_avg_pollution(map)

    # Define the impact of rain on pollution reduction
    precipitation_effect = CLOUD_EFFECTS.get(cloud, 0) if cloud == 'rain' else 0
    BASED_GROWTH_POLLUTION = abs(pollution - global_average_pollution) //  0.02 * pollution
    # Calculate the raw pollution change based on the contributing factors using "Weighted Pollution Balance Equation"
    raw_new_pollution = (
        POLLUTION_WEIGHTS['alpha'] * pollution +  
        POLLUTION_WEIGHTS['beta'] * pollution_avg +  
        gen_pollution -  
        absorb_pollution +  
        wind_pollution +  
        precipitation_effect +
        BASED_GROWTH_POLLUTION
    )
    # Smooth the pollution change using a dampening factor for gradual transitions
    new_pollution = pollution + DAMPENING_FACTOR['pollution_dampening'] * (abs(raw_new_pollution - pollution) * 0.05 * global_average_pollution)

    # Ensure pollution value that returns shows growth
    return max(pollution, new_pollution)

def calc_wind_direction(map_gen, cell):
    """
    Determine the predominant wind direction for a cell based on:
    - Temperature differences between the cell and its neighbors.

    Logic:
    - Identifies the neighbor with the highest temperature difference.
    - Assigns wind direction towards that neighbor.

    Returns:
    - next_direction (str): One of 'N', 'S', 'E', 'W'
    """
    # Get the list of neighbors for the current cell
    neighbors = map_gen.get_neighbors(cell.x, cell.y)
    
    # Calculate the absolute temperature differences between the cell and its neighbors
    temp_differences = calc_temp_difference(cell, neighbors)
    
    # Initialize variables to store the maximum temperature difference and its direction
    max_diff = -1 
    
    for i, neighbor in enumerate(neighbors):
        if temp_differences[i] > max_diff:
            # Update the maximum difference and determine the direction based on neighbor position
            max_diff = temp_differences[i]
            if neighbor.x < cell.x:  
                next_direction = 'E'
            elif neighbor.x > cell.x:  
                next_direction = 'W'
            elif neighbor.y > cell.y: 
                next_direction = 'N'
            else: 
                next_direction = 'S'
    
    # Return the determined wind direction
    return next_direction


def calc_wind_speed(map_gen, cell):
    """
    Calculate the wind speed at a cell based on:
    - Temperature differences with neighbors
    - Environmental factors like terrain type.

    Logic:
    - Uses squared differences in temperature for a base wind speed.
    - Applies terrain-based modifiers (e.g., higher over sea, lower in cities).

    Returns:
    - wind_speed (float) : The capped wind speed after applying modifiers.
    """
    neighbors = map_gen.get_neighbors(cell.x, cell.y)
    temp_differences = calc_temp_difference(cell, neighbors)
    total_squared_diff = sum(diff ** 2 for diff in temp_differences)
    wind_modifier = WIND_MODIFIER_MAP[cell.element]
    # Base wind speed calculation
    base_wind_speed = SCALING_FACTOR * math.sqrt(total_squared_diff) * wind_modifier
    # Apply the modifier and cap the wind speed
    wind_speed = min(max(base_wind_speed, 0.1), 5.0)  # Cap speed between 0.1 and 5.0
    return wind_speed


def calc_cloud_state(map_gen, cell, cloud_threshold, rain_threshold):
    """
    Determine the cloud state for a cell in the next iteration.

    Logic:
    - If the cell has no clouds but has at least `cloud_threshold` neighboring clouds, it becomes a cloud.
    - If the cell already has a cloud and has at least `rain_threshold` neighboring clouds, it becomes rain.
    - If the cell already has rain, it transitions to clear skies ('').
    
    Parameters:
    - cloud_threshold (int): Number of neighboring clouds required to form a cloud.
    - rain_threshold (int): Number of neighboring clouds required for cloud to transition to rain.

    Returns:
    - cloud state (str): One of 'rain', 'cloud', or '' for no clouds.
    """
    neighbors = map_gen.get_neighbors(cell.x, cell.y)
    cloud_neighbors = sum(1 for neighbor in neighbors if neighbor.get_cloud() == 'cloud')
    current_cloud_state = cell.get_cloud()

    # Logic for cloud state transitions
    if current_cloud_state == 'rain':
        # If the cell is rain, it transitions to clear skies
        return ''
    elif current_cloud_state == 'cloud':
        # If the cell is a cloud and has sufficient neighbors, it becomes rain
        if cloud_neighbors >= rain_threshold:
            return 'rain'
        return 'cloud'  # Retain cloud state if rain condition is not met
    elif current_cloud_state == '':
        # If the cell has no clouds but sufficient neighbors, it becomes a cloud
        if cloud_neighbors >= cloud_threshold:
            return 'cloud'
        return ''  # Remain clear if no condition is met


