import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk

# Function to update the plot based on speed and brake acceleration
def update_plot(speed, brake_acceleration):
    # Generate time data
    time = np.linspace(0, 10, 100)  # 0 to 10 seconds

    # Calculate distance based on speed and brake acceleration
    # Assuming constant deceleration
    distance = speed * (time / 3.6) + 0.5 * brake_acceleration * (time ** 2)

    # Clear the previous plot and create a new one
    ax.clear()
    ax.plot(time, distance, label=f'Speed = {speed} km/h, Brake = {brake_acceleration} m/s²', color='blue', marker='o')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Distance (m)')
    ax.set_title('Distance vs Time (Affected by Speed and Brake Acceleration)')
    ax.legend()
    canvas.draw()

# Function to handle slider updates
def on_slider_update(*args):
    speed = speed_slider.get()
    brake_acceleration = brake_slider.get()
    update_plot(speed, brake_acceleration)

# Create the main Tkinter window
root = tk.Tk()
root.title("Speed and Brake Acceleration Dashboard")

# Create the Matplotlib figure and axis
fig, ax = plt.subplots(figsize=(8, 6))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Initialize sliders
control_frame = tk.Frame(root)
control_frame.pack(side=tk.BOTTOM, fill=tk.X)

# Speed Slider
speed_label = tk.Label(control_frame, text="Speed (km/h):")
speed_label.pack(side=tk.LEFT, padx=5)
speed_slider = ttk.Scale(control_frame, from_=0, to=200, orient='horizontal', length=400, command=on_slider_update)
speed_slider.set(60)  # Default value
speed_slider.pack(side=tk.LEFT, padx=5)

# Brake Acceleration Slider
brake_label = tk.Label(control_frame, text="Brake Acceleration (m/s²):")
brake_label.pack(side=tk.LEFT, padx=5)
brake_slider = ttk.Scale(control_frame, from_=-10, to=0, orient='horizontal', length=400, command=on_slider_update)
brake_slider.set(-5)  # Default value
brake_slider.pack(side=tk.LEFT, padx=5)

# Initial plot
update_plot(speed_slider.get(), brake_slider.get())

# Start the Tkinter event loop
root.mainloop()
