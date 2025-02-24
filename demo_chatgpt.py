import numpy as np
import scipy.io.wavfile as wav
import resampy
import matplotlib.pyplot as plt

def normalize_audio(data):
    """ Normalize audio to the range [-1, 1] """
    return data / np.max(np.abs(data))

def dynamic_resample_fixed(input_wav, output_wav, speed_function):
    # Read the WAV file
    sample_rate, data = wav.read(input_wav)

    # Convert stereo to mono if needed
    if len(data.shape) > 1:
        data = np.mean(data, axis=1)

    # Normalize audio before processing to prevent clipping
    data = normalize_audio(data.astype(np.float32))
    #data = np.flip(data)

    num_samples = len(data)
    time_original = np.linspace(0, num_samples / sample_rate, num_samples)

    # Generate time-warped indices using the speed function
    speed_factors = speed_function(time_original)
    cumulative_time = np.cumsum(1 / speed_factors) / sample_rate
    plt.plot(cumulative_time)
    plt.show()

    # Interpolate new samples based on the warped time axis
    new_sample_count = int(cumulative_time[-1] * sample_rate)
    new_time = np.linspace(0, cumulative_time[-1], new_sample_count)
    new_data = np.interp(new_time, cumulative_time, data)

    # Normalize audio after processing to prevent clipping
    new_data = normalize_audio(new_data)

    # Convert back to original dtype
    new_data = (new_data * 32767).astype(np.int16)  # Convert back to 16-bit PCM

    # Save the new WAV file
    wav.write(output_wav, sample_rate, new_data)

    # # Debug: Plot original and modified time mappings
    # plt.figure(figsize=(10, 5))
    # plt.plot(time_original, speed_factors, label="Speed Factor", color='red')
    # plt.xlabel("Time (s)")
    # plt.ylabel("Speed Factor")
    # plt.title("Speed Variation Over Time")
    # plt.legend()
    # plt.show()

# Example speed function: Smooth oscillation
def speed_function(time):
    return 0.5 * np.sin(2 * np.pi * 0.2 * time)  # Speed oscillates

# Usage
dynamic_resample_fixed("makso.wav", "output_dynamic_fixed.wav", speed_function)
