from audio_output import AudioOutput
from player import Player
from processor import Processor
import numpy as np
import scipy.signal as sig
import soundfile as sf

FS = 44100
#FS = 1600
BS = 512
CHANNELS = 1

f = 900

length = 60
samples = np.linspace(0, length, int(FS*length))
signal = 0.5 * np.sin(2 * np.pi * f * samples)
#signal = 0.5 * sig.square(2 * np.pi * f * samples, 0.5)
fs = FS

signal, fs = sf.read("intro3.wav")

if len(signal.shape) > 1:
    #signal = np.mean(signal, axis=1)
    signal = signal[:,0]

out = AudioOutput(fs, BS, CHANNELS)
player = Player(signal, out, fast_forward_speed = 2, ramp_time = 1)
