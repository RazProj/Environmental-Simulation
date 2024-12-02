import os
import numpy as np

def calculate_map_averages(map, map_size, avg_temp_label, avg_pollution_label, std_temp_label, std_pollution_label):
    """
    Calculate and display the average temperature and pollution, along with their standard deviations.
    Append the averages to corresponding files.
    """
    total_temp = 0
    total_pollution = 0
    temp_values = []
    pollution_values = []

    # Iterate through the map and collect temperature and pollution values
    for row in map:
        for cell in row:
            temp = cell.get_temp()
            pollution = cell.get_pollution()
            temp_values.append(temp)
            pollution_values.append(pollution)
            total_temp += temp
            total_pollution += pollution

    # Calculate averages and standard deviations
    num_cells = map_size ** 2
    avg_temp = total_temp / num_cells
    avg_pollution = total_pollution / num_cells
    std_temp = np.std(temp_values)
    std_pollution = np.std(pollution_values)

    # Update UI labels
    avg_temp_label.config(text=f"Average Temperature: {avg_temp:.2f}")
    avg_pollution_label.config(text=f"Average Pollution: {avg_pollution:.3f}%")
    std_temp_label.config(text=f"Standard Deviation - Temperature: {std_temp:.3f}")
    std_pollution_label.config(text=f"Standard Deviation - Pollution: {std_pollution:.3f}")

    # Append average temperature to file
    temp_file_path = "average_temperature.txt"
    with open(temp_file_path, "a") as temp_file:
        temp_file.write(f"{avg_temp:.2f}\n")

    # Append average pollution to file
    pollution_file_path = "average_pollution.txt"
    with open(pollution_file_path, "a") as pollution_file:
        pollution_file.write(f"{avg_pollution:.3f}\n")

def check_and_update_cell_type(cell):
    """
    Check if a cell's temperature is beyond a threshold and update its type accordingly.

    Rules:
    - Forest becomes land if temp > 40.
    - Glacier becomes sea if temp >= 0 and vice versa.
    - Cities become land if temp > 50.
    """

    # Get the current type and temperature
    current_type = cell.element
    current_temp = cell.get_temp()

    # Apply rules
    if current_type == 'forest' and current_temp > 40:
        cell.element = 'land'
    elif current_type == 'glacier' and current_temp >= 0:
        cell.element = 'sea'
    elif current_type == 'sea' and current_temp < 0:
        cell.element = 'glacier'
    elif current_type == 'city' and current_temp > 50:
        cell.element = 'land'

def delete_files(file_paths):
    """Deletes the specified files."""
    for file_path in file_paths:
        try:
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")

def add_clouds_to_glaciers(map, map_size, iteration):
    """Add clouds to glacier at the beginning and let the CA change them."""
    if iteration == 1:  # Trigger on specific iterations
        for i in range(map_size):  # Loop through all rows
            for j in range(map_size):  # Loop through all columns
                cell = map[i][j]
                
                # Check if the cell is a glacier and does not already have a cloud
                if cell.element == 'glacier' and cell.get_cloud() == '':
                    cell.set_cloud('cloud')  # Add a cloud to the glacier cell