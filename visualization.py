import matplotlib.pyplot as plt
import numpy as np

def read_averages(file_path):
    """Reads averages from a file and returns a list of floats."""
    averages = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                value = float(line.strip())
                averages.append(value)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except ValueError:
        print(f"Non-numeric data encountered in {file_path}.")
    return averages


def plot_combined_with_separate_std_and_normalized(temp_averages, pollution_averages):
    """
    Plots temperature, pollution averages, their respective standard deviations,
    and normalized values for both in the same window.
    """
    days = range(1, len(temp_averages) + 1)  # Each value corresponds to a day

    fig, axes = plt.subplots(2, 2, figsize=(14, 12))  # Create a 2x2 grid of subplots

    # Plot standard deviation of temperature
    temp_std_devs = [np.std(temp_averages[:i]) for i in range(1, len(temp_averages) + 1)]
    axes[0, 0].plot(days, temp_std_devs, label="Temperature Std Dev", marker='o', linestyle='-', color='orange')
    axes[0, 0].set_title("Temperature Standard Deviation Over Days")
    axes[0, 0].set_xlabel("Days")
    axes[0, 0].set_ylabel("Standard Deviation")
    axes[0, 0].legend()
    axes[0, 0].grid(True)

    # Plot standard deviation of pollution
    pollution_std_devs = [np.std(pollution_averages[:i]) for i in range(1, len(pollution_averages) + 1)]
    axes[0, 1].plot(days, pollution_std_devs, label="Pollution Std Dev", marker='x', linestyle='--', color='purple')
    axes[0, 1].set_title("Pollution Standard Deviation Over Days")
    axes[0, 1].set_xlabel("Days")
    axes[0, 1].set_ylabel("Standard Deviation")
    axes[0, 1].legend()
    axes[0, 1].grid(True)

    # Plot normalized temperature
    temp_yearly_avg = np.mean(temp_averages)
    temp_yearly_std = np.std(temp_averages)
    normalized_temp = [(value - temp_yearly_avg) / temp_yearly_std for value in temp_averages]
    axes[1, 0].plot(days, normalized_temp, label="Normalized Temperature", marker='o', linestyle='-', color='green')
    axes[1, 0].axhline(y=0, color='red', linestyle='--', label="Yearly Avg (Normalized)")
    axes[1, 0].set_title("Normalized Temperature Over Days")
    axes[1, 0].set_xlabel("Days")
    axes[1, 0].set_ylabel("Normalized Value")
    axes[1, 0].legend()
    axes[1, 0].grid(True)

    # Plot normalized pollution
    pollution_yearly_avg = np.mean(pollution_averages)
    pollution_yearly_std = np.std(pollution_averages)
    normalized_pollution = [(value - pollution_yearly_avg) / pollution_yearly_std for value in pollution_averages]
    axes[1, 1].plot(days, normalized_pollution, label="Normalized Pollution", marker='x', linestyle='--', color='brown')
    axes[1, 1].axhline(y=0, color='red', linestyle='--', label="Yearly Avg (Normalized)")
    axes[1, 1].set_title("Normalized Pollution Over Days")
    axes[1, 1].set_xlabel("Days")
    axes[1, 1].set_ylabel("Normalized Value")
    axes[1, 1].legend()
    axes[1, 1].grid(True)

    # Adjust layout
    plt.tight_layout()
    plt.show()
