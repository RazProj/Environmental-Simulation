import tkinter as tk
import time
import random
from map import MapGenerator
from cell import Cell
from calculations import (
    calc_temp,
    calc_pollution,
    calc_wind_speed,
    calc_wind_direction,
    calc_cloud_state

)
from visualization import read_averages, plot_combined_with_separate_std_and_normalized
from calculation_utils import increase_get_pollution
from simulation_utils import (
    calculate_map_averages,
    check_and_update_cell_type,
    delete_files,
    add_clouds_to_glaciers,
)

# Constants
CELL_COLORS = {
    'city': 'grey',
    'forest': 'green',
    'sea': 'skyblue',
    'land': 'saddlebrown',
    'glacier': 'white'
}
CLOUD_ICONS = {
    'cloud': "☁",
    'rain': "🌧",
    '': ""
}

class SimulationApp:
    def __init__(self, root, map_size, iterations):
        """
        Initialize the simulation app with UI components and simulation setup.
        """
        self.root = root
        self.root.title("Environmental Simulation")

        self.map_size = map_size
        self.iterations = iterations
        self.map_generator = MapGenerator(map_size)
        self.map = self.map_generator.map

        # UI Components
        self.canvas_size = 800
        self.cell_size = max(30, self.canvas_size // self.map_size)  # Adaptive cell size
        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size)
        self.canvas.grid(row=0, column=0, rowspan=2)

        self.info_frame = tk.Frame(root)
        self.info_frame.grid(row=0, column=1, padx=20)

        self.avg_temp_label = tk.Label(self.info_frame, text="Average Temperature: N/A")
        self.avg_temp_label.pack()

        self.avg_pollution_label = tk.Label(self.info_frame, text="Average Pollution: N/A")
        self.avg_pollution_label.pack()

        self.std_temp_label = tk.Label(self.info_frame, text="Standard Deviation - Temperature: N/A")
        self.std_temp_label.pack()

        self.std_pollution_label = tk.Label(self.info_frame, text="Standard Deviation - Pollution: N/A")
        self.std_pollution_label.pack()

        self.start_button = tk.Button(self.info_frame, text="Start Simulation", command=self.start_simulation)
        self.start_button.pack()

        self.update_grid()

    def update_grid(self):
        """
        Update the visualization grid to reflect current cell states.
        """
        self.canvas.delete("all")
        self.cell_size = max(30, self.canvas_size // self.map_size)
        for i in range(self.map_size):
            for j in range(self.map_size):
                cell = self.map[i][j]
                x1, y1 = j * self.cell_size, i * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size

                # Draw cell background
                color = CELL_COLORS[cell.element]
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

                # Display temperature
                self.canvas.create_text(
                    (x1 + x2) // 2, y1 + self.cell_size // 4,
                    text=f"{cell.get_temp():.1f}°", font=("Arial", max(6, self.cell_size // 5)), fill="black"
                )

                # Display pollution
                self.canvas.create_text(
                    (x1 + x2) // 2, y2 - self.cell_size // 4,
                    text=f"{cell.get_pollution():.3f}", font=("Arial", max(6, self.cell_size // 5)), fill="black"
                )

                # Display cloud icon
                cloud_state = cell.get_cloud() or ''  # Default to '' if get_cloud() returns None
                cloud_icon = CLOUD_ICONS.get(cloud_state, '')  # Default to '' if cloud_state is invalid
                self.canvas.create_text(
                    (x1 + x2) // 2, (y1 + y2) // 2,
                    text=cloud_icon, font=("Arial", max(8, self.cell_size // 3)), fill="blue"
                )

    def update_simulation(self):
        """
        Perform a simulation step by updating temperature, pollution, clouds, and wind for all cells.
        """
        next_map = [[None for _ in range(self.map_size)] for _ in range(self.map_size)]

        for i in range(self.map_size):
            for j in range(self.map_size):
                cell = self.map[i][j]
                next_cell = Cell(cell.x, cell.y, cell.element)
                next_cell.set_temp(calc_temp(self.map, self.map_generator, cell))
                next_cell.set_pollution(calc_pollution(self.map, self.map_generator, cell))
                next_cell.set_cloud(calc_cloud_state(self.map_generator, cell, random.randint(0, 3), random.randint(0, 3)))
                next_cell.set_wind_speed(calc_wind_speed(self.map_generator, cell))
                next_cell.set_wind_direction(calc_wind_direction(self.map_generator, cell))
                check_and_update_cell_type(next_cell)
                increase_get_pollution(next_cell)

                next_map[i][j] = next_cell

        self.map = next_map

    def start_simulation(self):
        """
        Start the simulation loop for the defined number of iterations.
        """
        self.start_button.config(state=tk.DISABLED)

        for iteration in range(1, self.iterations + 1):
            add_clouds_to_glaciers(self.map, self.map_size, iteration)
            self.update_simulation()
            self.update_grid()
            # update_clouds(self.map, self.map_generator, self.map_size, iteration, cloud_lifecycles)
            calculate_map_averages(
                self.map, self.map_size,
                self.avg_temp_label, self.avg_pollution_label,
                self.std_temp_label, self.std_pollution_label
            )

            self.root.update()
            time.sleep(0.0001)
        root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SimulationApp(root, map_size=20, iterations=365)
    root.mainloop()

    # File paths
    temp_file = "average_temperature.txt"
    pollution_file = "average_pollution.txt"

    # Read data from files
    temperature_averages = read_averages(temp_file)
    pollution_averages = read_averages(pollution_file)

    # Check if both data sets have values
    if temperature_averages and pollution_averages:
        plot_combined_with_separate_std_and_normalized(temperature_averages, pollution_averages)
    else:
        print("Ensure both files contain data.")

        # Delete the files after showing the visualization
    delete_files(["average_temperature.txt", "average_pollution.txt"])
