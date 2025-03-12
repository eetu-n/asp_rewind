import numpy as np
import scipy.io.wavfile as wav
import soundfile as sf
from matplotlib import pyplot as plt
import resampy as rs
from speed import speed_function

OUT_BLOCK_SIZE = 1024

class Processor():
    def __init__(self):
        self.signal = []
        self.forward = True
        self.current_sample = 0
        self.signal_fs = 0
        self.current_fs = 0
        
    def add_signal(self, signal_in):
        # Which one?
        #self.signal = np.concatenate([self.signal, signal_in],0)
        self.signal = np.append(self.signal, signal_in)

    def change_rate(self, fs):
        self.current_fs = fs
        if fs > 0:
            self.forward = True
        else:
            self.forward = False

    def get_input_sample_number(self):
        return OUT_BLOCK_SIZE * self.current_fs

    # Get one block of signal
    def get_block(self):
        start_idx = self.current_sample
        end_idx = self.current_sample

        # Update start and end indices
        num_samples = self.get_input_sample_number()
        if self.forward:
            end_idx = min(start_idx + num_samples, len(self.signal)-1)
            self.current_sample = end_idx
        else:
            start_idx = min(end_idx - num_samples, 0)
            self.current_sample = start_idx

        return self.signal[start_idx:end_idx]

    def resample(self, signal_in):
        return rs.resample(signal_in, self.current_fs)
    
    # Returns the signal to be played (1024 samples)
    def play(self):
        # Check that there is signal to play, else return
        if self.current_sample < 0 or self.current_sample >= len(self.signal):
            return
        
        signal_in = signal_in = self.get_block()
        signal_out = np.zeros(OUT_BLOCK_SIZE) # Fixed size

        # Flip signal if going backwards
        if not self.forward:
            signal_in = np.flip(signal_in)

        # Change sample rate if needed
        if self.signal_fs != self.current_fs:
           signal_in = self.resample(signal_in)

        # Pad with zeros if ran out of signal
        signal_out[0,len(signal_in)] = signal_in

        return signal_out
    
            

        

    
