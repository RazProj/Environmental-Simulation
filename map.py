import cell 

class MapGenerator:
    def __init__(self, size):
        # Check if the size is valid (must be 10 or greater)
        if size < 10:
            raise ValueError("Map size must be 10 or greater.")
        
        self.size = size  # Store the size of the map
        self.map = self.create_map()  # Initialize the map grid by calling the create_map() method

    def create_map(self):
        """Creates and populates the map with cells."""
        # Initialize a 2D list (grid) with all cells set to 0 initially
        map_grid = [([0] * self.size) for _ in range(self.size)]
        
        # Populate the map with actual Cell objects
        for i in range(self.size):
            for j in range(self.size):
                map_grid[i][j] = self.create_cell(i, j)
                
        return map_grid 

    def create_cell(self, i, j):
        """
        Creates a cell with a specific element based on its position (i, j).
        The map is divided into different regions (sea, glacier, forest, land, city).
        """
        sea_border = self.size // 7  # Sea covers approximately 14% of the borders
        glacier_width = self.size // 6  # Glaciers occupy the four corners of the map
        land_start = self.size // 5  # Start of the land area (for cities)
        land_end = land_start + self.size // 4  # End of the land area (city region extended)

        # Determine the type of element for the current cell (i, j) based on its position
        if (i < glacier_width and j < glacier_width) or (i < glacier_width and j >= self.size - glacier_width) or \
           (i >= self.size - glacier_width and j < glacier_width) or (i >= self.size - glacier_width and j >= self.size - glacier_width):
            # If the cell is in one of the four corners, it is a glacier
            element = 'glacier'
        elif i < sea_border or j < sea_border or i >= self.size - sea_border or j >= self.size - sea_border:
            # If the cell is on the outer borders, it is sea
            element = 'sea'
        elif land_start <= i < land_end and land_start <= j < land_end:
            # If the cell is within the central region, it is part of the city
            element = 'land'
        elif (land_start - sea_border <= i < land_start or land_end <= i < land_end + sea_border) or \
             (land_start - sea_border <= j < land_start or land_end <= j < land_end + sea_border):
            # If the cell is in the buffer zone around the city, it is forest
            element = 'forest'
        else:
            # Any remaining cell in the map is considered as land
            element = 'city'
        
        # Create a Cell object with the determined element type
        return cell.Cell(i, j, element)

    def get_neighbors(self, i, j):
        """
        Get the north, south, east, and west neighbors of the cell at position (i, j).
        Returns a list of neighboring cells.
        """
        neighbors = []  # Initialize an empty list to store neighbors
        
        # Check if the cell has a north neighbor (i-1, j)
        if i > 0:
            neighbors.append(self.map[i - 1][j])
        
        # Check if the cell has a south neighbor (i+1, j)
        if i < self.size - 1:
            neighbors.append(self.map[i + 1][j])
        
        # Check if the cell has a west neighbor (i, j-1)
        if j > 0:
            neighbors.append(self.map[i][j - 1])
        
        # Check if the cell has an east neighbor (i, j+1)
        if j < self.size - 1:
            neighbors.append(self.map[i][j + 1])
        
        return neighbors  # Return the list of neighboring cells
