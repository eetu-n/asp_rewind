import numpy as np
from matplotlib import pyplot as plt

time = np.linspace(0, 430*1024, 430)
#print(time)

def speed_function(ratio=2, ramp_on=False, flutter=False, prev_ratio=1, ramp_blocks=1, flutter_time=1, block_size = 1024):
    """
    Generates a vector of sampling rate values for block processing.

    Parameters:
    - time (numpy array): Time values over which the speed function is computed.
    - ratio (float, optional): Scaling factor for the speed, used for "constant" and "ramp" modes.
    - ramp (Boolean, optional): Whether to have a ramp to target ratio
    - flutter (Boolean, optional): Whether to vary the target ratio
    - prev_ratio (int, required if ramp=true): Where to ramp from
    """
    total_time = ramp_blocks + flutter_time
    time = np.linspace(0, total_time*block_size, total_time)
    if not ramp_on:
        function = np.ones(total_time)*ratio
    else:
        ratio_diff = ratio - prev_ratio
        ramp_start = 0
        ramp_end = time[ramp_blocks]
        ramp = np.ones_like(time) * ratio
        function = np.where((time >= ramp_start) & (time <= ramp_end), (time / ramp_end) * ratio_diff + prev_ratio, ramp)

    if flutter:
        function = 1+ 0.5 * np.sin(2 * np.pi * 0.2 * time)  # Speed oscillates

    function = np.where((function >= 0) & (function <= 0.1), 0.1, function)
    function = np.where((function <= 0) & (function >= -0.1), -0.1, function)
    # Plot the function
    #plt.plot(time, function)
    #plt.show()
    return function

_ = speed_function()