import importlib
import UTILS
importlib.reload(UTILS)
from UTILS import *

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
import scipy

import soundfile as sf

#signal, fs = sf.read("square_sweep.wav")

fs = 44100

ellip_b, ellip_a = sig.ellip(6, 1, 60, 1000, fs = fs)

bode_plot(a = ellip_a, b=ellip_b, fs = fs, title="Elliptic Filter Frequency Response", save=True)
