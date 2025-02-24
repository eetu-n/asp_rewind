import numpy as np
import scipy.io.wavfile as wav
import resampy
import matplotlib.pyplot as plt

def normalize_audio(data):
    """ Normalize audio to the range [-1, 1] """
    return data / np.max(np.abs(data))
import numpy as np
import scipy.io.wavfile as wav
import resampy

def dynamic_resample(input_wav, output_wav, speed_function, chunk_size=1024):
    # Read the WAV file
    sample_rate, data = wav.read(input_wav)
    if len(data.shape) > 1:  # Convert stereo to mono if needed
        data = np.mean(data, axis=1)

    num_samples = len(data)
    time = np.linspace(0, len(data) / sample_rate, num_samples)
    data = normalize_audio(data)

    # Generate speed variation over time
    speed_factors = speed_function(time)

    # Process audio in small chunks
    output_audio = []
    start_idx = 0
    while start_idx < num_samples:
        end_idx = min(start_idx + chunk_size, num_samples)

        # Compute the average speed factor for this chunk
        avg_speed = np.mean(speed_factors[start_idx:end_idx])
        new_chunk_size = int(chunk_size / avg_speed)

        # Resample the chunk
        resampled_chunk = resampy.resample(
            data[start_idx:end_idx].astype(np.float32), sample_rate, int(sample_rate * avg_speed)
        )
        output_audio.append(resampled_chunk)

        start_idx = end_idx  # Move to the next chunk

    # Concatenate resampled chunks
    output_audio = np.concatenate(output_audio).astype(data.dtype)

    # Save new WAV file
    wav.write(output_wav, sample_rate, output_audio)

# Example: Speed oscillates between 0.5x and 2x over time
def speed_function(time):
    return 1 + 0.5 * np.sin(2 * np.pi * 0.2 * time)  # Speed varies smoothly

# Usage
dynamic_resample("makso.wav", "output_dynamic.wav", speed_function)
