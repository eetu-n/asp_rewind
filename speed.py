import numpy as np
from matplotlib import pyplot as plt

time = np.linspace(0, 10, 1000)

def speed_function(time, type="constant", ratio=2):
    """
    Generates a vector of sampling rate values for block processing.

    Parameters:
    - time (numpy array): Time values over which the speed function is computed.
    - type (str, optional): Type of speed variation.
        - "constant": A constant speed multiplier.
        - "ramp": A trapezoidal speed profile with linear acceleration and deceleration.
        - "flutter": A sinusoidal variation in speed.
    - ratio (float, optional): Scaling factor for the speed, used for "constant" and "ramp" modes.
    """
    if type=="constant":
        ramp = np.ones_like(time)*ratio
    if type=="ramp":
        slope_length = time[-1]//10
        rise_start = 0
        rise_end = slope_length
        ramp = np.ones_like(time)
        ramp = np.where((time >= rise_start) & (time <= rise_end), (time - 0) / slope_length, ramp)

        # Plateau (1)
        flat_start = slope_length
        flat_end = time[-1] - slope_length
        ramp = np.where((time > flat_start) & (time < flat_end), 1, ramp)

        # Falling edge (1 to 0)
        fall_start = flat_end
        fall_end = time[-1]
        ramp = np.where((time >= fall_start) & (time <= fall_end), 1 - (time - fall_start) / slope_length, ramp)
        function = ramp*ratio

    if type == "flutter":
        function = 1+ 0.5 * np.sin(2 * np.pi * 0.2 * time)  # Speed oscillates

    # Plot the function
    plt.plot(time, function)
    plt.show()
    return function

_ = speed_function(time, type="flutter", ratio=-2)