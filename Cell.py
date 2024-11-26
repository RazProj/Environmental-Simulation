class Cell:
    ELEMENT_ATTRIBUTES = {
        'sea': {'temp': 20, 'pollution': 0.02, 'wind_direction': 'E', 'wind_speed': 0.2},
        'forest': {'temp': 15, 'pollution': 0.01, 'wind_direction': 'N', 'wind_speed': 0.1},
        'land': {'temp': 25, 'pollution': 0.03, 'wind_direction': 'S', 'wind_speed': 0.3},
        'city': {'temp': 25, 'pollution': 0.05, 'wind_direction': 'E', 'wind_speed': 0.2},
        'glaciers': {'temp': -10, 'pollution': 0.02, 'wind_direction': 'W', 'wind_speed': 0.5},
    }

    TEMP_WEIGHTS = {
        'alpha': 0.5,
        'beta': 0.3,
        'gamma': 0.1,
        'delta': 0.1
    } # Weights values for linear weighted update equation which calculates the next temp.

    POLLUTION_WEIGHTS = {
        'alpha': 0.4,
        'beta': 0.2
    }

    def __init__(self, x, y, element):
        self.x = x
        self.y = y
        self.element = element
        self.attributes_val = self.ELEMENT_ATTRIBUTES.get(element)
    
    def cal_temp(self):
        temperature = self.attributes_val['temp']
        temp_avg = self.cal_avg('temp')
        pollution = self.attributes_val['pollution']
        wind_avg = self.cal_W('temp')
        return self.TEMP_WEIGHTS['alpha'] * temperature + self.TEMP_WEIGHTS['beta'] * temp_avg + self.TEMP_WEIGHTS['gamma'] * pollution + self.TEMP_WEIGHTS['delta'] * wind_avg
        
        

    def cal_avg(self, attribute):
        neighbors = map.get_neighbors(self.x, self.y) # Return list of Cells objects
        attribute_sum = 0
        for neighbor in neighbors:
            neighbor_attribute = neighbor.attributes_val[attribute]
            attribute_sum += neighbor_attribute
        return attribute_sum / len(neighbors)
    
    def cal_W(self, attribute):
        neighbors = map.get_neighbors(self.x, self.y) # Return list of Cells objects
        neighbors = self.towards_neighbors(neighbors)
        wind_sum = 0
        cell_wind_speed = self.attributes_val['wind_speed']
        for neighbor in neighbors :
            neighbor_attribute = neighbor.attributes_val[attribute]
            self_attribute = self.attributes_val[attribute]
            wind_sum += cell_wind_speed * (neighbor_attribute - self_attribute)
        return wind_sum / len(neighbors)

    def towards_neighbors(self, neighbors):
        temp = []
        for neighbor in neighbors:
            neighbor_wind_direction = neighbor.attributes_val['wind_direction']
            
            # Check for wind alignment
            if neighbor_wind_direction == 'S' and neighbor.x == self.x and neighbor.y > self.y:
                temp.append(neighbor)  # Wind from North (S) towards this cell
            elif neighbor_wind_direction == 'N' and neighbor.x == self.x and neighbor.y < self.y:
                temp.append(neighbor)  # Wind from South (N) towards this cell
            elif neighbor_wind_direction == 'E' and neighbor.y == self.y and neighbor.x < self.x:
                temp.append(neighbor)  # Wind from West (E) towards this cell
            elif neighbor_wind_direction == 'W' and neighbor.y == self.y and neighbor.x > self.x:
                temp.append(neighbor)  # Wind from East (W) towards this cell

        return temp

