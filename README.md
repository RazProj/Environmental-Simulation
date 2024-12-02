# Environmental Simulation Project

This project simulates environmental changes over time using cellular automata principles, modeling dynamic interactions of temperature, pollution, wind, and cloud states within a grid environment that represents various natural and urban regions.

## Features
- **Temperature Dynamics**: Tracks changes based on local conditions and neighboring cells.
- **Pollution Spread**: Models the generation, absorption, and movement of pollution.
- **Wind Simulation**: Calculates wind speed and direction based on temperature differences.
- **Cloud and Rain Formation**: Implements clouds transitioning into rain and dispersing based on neighbors curret cloud state
- **Visualization**: Displays grid states and plots statistical trends over time.

---

## Project Structure

### Root Directory

### Key Files
- **map.py**: Handles grid creation and neighbor calculations.
- **cell.py**: Defines the properties and behaviors of individual cells.
- **calculation_utils.py**: Contains utility functions for calculations such as averages and differences.
- **calculations.py**: Implements the core logic for temperature, pollution, wind, and cloud state calculations.
- **simulation_utils.py**: Provides helper functions for simulation and statistical analysis.
- **visualization.py**: Generates plots to visualize data trends.
- **simulation.py**: Main script for running the simulation and rendering the environment.

---

## How to Run

1. **Install Dependencies**
   - Ensure Python 3.10+ is installed.
   - Install required libraries using:
     ```bash
     pip install matplotlib numpy
     ```

2. **Execute the Simulation**
   - Run the `simulation.py` script:
     ```bash
     python simulation.py
     ```

3. **Visualizations**
   - Once the simulation is complete, visualizations will be displayed, showing trends in temperature and pollution over time with normalized standard deviation analysis.

---

## Usage

### Simulation Grid
- Each cell in the grid represents a region (e.g., sea, city, forest, glacier, land).
- Attributes include:
  - Temperature
  - Pollution in the region
  - Wind Speed and Direction
  - The quantity of pollution the region is generating
  - The quantity of pollution the region is absrobing
  - Cloud State
![alt text](<mocks/attributes.png>)

### Cell Colors

- **City**: Grey
- **Land**: Brown
- **Sea**: Light Blue
- **Glacier**: White
- **Forest**: Green

### Interactions
- Temperature and pollution evolve based on local conditions and global averages. Temperature and pollution also evolve using the average conditions of neighboring cells.
- Wind affects pollution and temperature propagation.
- Clouds form based on neighboring conditions.

---
## Global Factors and Weightsg

The simulation integrates both local and global factors to simulate realistic environmental changes:

### Global Factors

- **Global Average Temperature**: Influences baseline temperature growth and ensures alignment with overall trends.
- **Global Average Pollution**: Affects the pollution growth rate and amplifies or dampens changes across the grid.

### Weights

- **Temperature Weights**:
  - **Alpha**: Impact of the cell’s own temperature.
  - **Beta**: Influence of neighboring cell temperatures.
  - **Gamma**: Contribution of pollution to temperature growth.
  - **Delta**: Effect of wind speed and direction.
- **Pollution Weights**:
  - **Alpha**: Contribution of the cell’s own pollution level.
  - **Beta**: Influence of pollution levels in neighboring cells.

These weights are calibrated for different cell types (e.g., city, glacier) to mimic their real-world environmental dynamics.

---
## Functions Overview

### `calculations.py`
1. **`calc_temp()`**
   - Computes new temperature for a cell based on:
     - Cell’s current state
     - Neighboring cells’ average temperature
     - Pollution and wind impact
   - Incorporates dampening factors for realistic changes.

2. **`calc_pollution()`**
   - Updates pollution considering:
     - Local generation and absorption
     - Neighbor influence
     - Wind effects
     - Rain-induced pollution reduction.

3. **`calc_wind_direction()`**
   - Determines predominant wind direction based on neighboring temperature differences.

4. **`calc_cloud_state()`**
   - Models cloud transitions based on neighboring cells and random thresholds.

### `visualization.py`
1. **`plot_combined_with_separate_std_and_normalized()`**
   - Plots temperature and pollution trends:
     - Standard deviation over time
     - Normalized values to observe fluctuations.

2. **`read_averages()`**
   - Reads temperature and pollution averages from files for plotting.

---

## Example Output

1. **Grid Display**
   - Temperature and pollution values are rendered on a grid with visual indicators for clouds and rain.
![alt text](<mocks/grid_map_during_running.jpg>) 

2. **Statistical Trends**
   - Plots showcasing:
     - Daily temperature and pollution fluctuations
     - Standard deviation trends
     - Normalized growth metrics.
![alt text](<mocks/statisticals.png>)
---

## Development Notes
- Ensure the mock folder is inside the root directory for seamless access to resources.
- Modify weights in `calculations.py` to experiment with environmental dynamics.

---

## Future Enhancements
1. Implement dynamic user input for grid size and simulation parameters.
2. Introduce more environmental factors (e.g., seasonal effects, natural disasters).
3. Optimize cloud lifecycle transitions for better realism.

---

## Contributors
- Raz Solomon - Developer

---

## License
This project is licensed under the MIT License.
