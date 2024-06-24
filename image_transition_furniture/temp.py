import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
import numpy as np

# Function to simulate sensor data
def get_sensor_data():
    return random.uniform(0, 100)

# Function to create and update all charts
def update_charts(frame, axes):
    categories = ['A', 'B', 'C', 'D', 'E']
    values = [get_sensor_data() for _ in categories]
    
    # Update Bar Chart
    axes[0, 0].clear()
    axes[0, 0].bar(categories, values)
    axes[0, 0].set_title("Real-Time Bar Chart")
    axes[0, 0].set_xlabel("Category")
    axes[0, 0].set_ylabel("Value")

    # Update Pie Chart
    axes[0, 1].clear()
    axes[0, 1].pie(values, labels=categories, autopct='%1.1f%%')
    axes[0, 1].set_title("Real-Time Pie Chart")

    # Update Line Chart
    x_data.append(frame)
    y_data.append(get_sensor_data())
    axes[1, 0].clear()
    axes[1, 0].plot(x_data, y_data)
    axes[1, 0].set_title("Real-Time Line Chart")
    axes[1, 0].set_xlabel("Time")
    axes[1, 0].set_ylabel("Sensor Value")

    # Update Hourglass Chart
    axes[1, 1].clear()
    axes[1, 1].plot(x_data, y_data, 'bo')
    axes[1, 1].plot(x_data, [-y for y in y_data], 'ro')
    axes[1, 1].set_title("Real-Time Hourglass Chart")
    axes[1, 1].set_xlabel("Time")
    axes[1, 1].set_ylabel("Sensor Value")

    # Update Density Chart
    x_density_data.append(random.uniform(0, 100))
    y_density_data.append(get_sensor_data())
    axes[2, 0].clear()
    axes[2, 0].hist2d(x_density_data, y_density_data, bins=[30, 30], cmap='Blues')
    axes[2, 0].set_title("Real-Time Density Chart")
    axes[2, 0].set_xlabel("X Value")
    axes[2, 0].set_ylabel("Sensor Value")

    # Update Location Chart
    latitudes.append(random.uniform(-90, 90))
    longitudes.append(random.uniform(-180, 180))
    axes[2, 1].clear()
    axes[2, 1].scatter(longitudes, latitudes)
    axes[2, 1].set_title("Real-Time Location Chart")
    axes[2, 1].set_xlabel("Longitude")
    axes[2, 1].set_ylabel("Latitude")

# Setup the figure and axes
fig, axes = plt.subplots(3, 2, figsize=(15, 10))
x_data, y_data = [], []
x_density_data, y_density_data = [], []
latitudes, longitudes = [], []

# Start the animation
ani = FuncAnimation(fig, update_charts, fargs=(axes,), interval=1000)

# Display the plots
plt.tight_layout()
plt.show()
