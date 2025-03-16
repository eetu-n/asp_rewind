from audio_output import AudioOutput
from player import Player
from processor import Processor
import numpy as np
import soundfile as sf

FS = 44100
BS = 128
CHANNELS = 1

length = 10
samples = np.linspace(0, length, int(FS*length))
signal = 0.5 * np.sin(2 * np.pi * 1000 * samples)
fs = FS

#signal, fs = sf.read("makso.wav")

if len(signal.shape) > 1:  
    #signal = np.mean(signal, axis=1)
    signal = signal[:,0]

out = AudioOutput(fs, BS, CHANNELS)
player = Player(signal, out)

