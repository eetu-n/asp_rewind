import importlib
import UTILS
importlib.reload(UTILS)
from UTILS import *

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
import scipy

import soundfile as sf

#signal, fs = sf.read("./audio/clicks.wav")
#
#sig_plot(signal, "Block Boundary Issues", int(fs*2), int(fs*2.01), w=10, h=2, save=True, show=False)
#sig_plot(signal, "Gradual Speed Change", int(fs*0.1), int(fs*0.4), w=10, h=2, save=True, show=False)
#
signal, fs = sf.read("./audio/aliasing.wav")

fft_plot(signal, fs, "Aliasing Effect", w=5, h=3, save=True)

signal, fs = sf.read("./audio/anti-aliasing.wav")

fft_plot(signal, fs, "Anti-Aliasing", w=5, h=3, save=True)

#fs = 44100
#
#ellip_b, ellip_a = sig.ellip(6, 5, 60, 1000, fs = fs)
#bode_plot(a = ellip_a, b=ellip_b, fs = fs, title="Elliptic Filter Frequency Response", save=True, w=5, h=3)
