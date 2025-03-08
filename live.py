from AudioOutput import AudioOutput
import numpy as np

CHUNK = 1024
fs = 44100

out = AudioOutput(fs, CHUNK, 1)

samples = np.linspace(0, 1, int(fs*1))
signal = 0.5 * np.sin(2 * np.pi * 1000 * samples)

n = 0
while n < len(signal):
    out.write(signal[n:n+CHUNK])
    n += CHUNK

out.close()