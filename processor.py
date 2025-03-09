import numpy as np
import scipy.io.wavfile as wav
import soundfile as sf
from matplotlib import pyplot as plt
import resampy as rs

BLOCK_SIZE = 1024


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

    # Get one block of signal
    def get_block(self):
        start_idx = self.current_sample
        end_idx = self.current_sample

        # Update start and end indices
        if self.forward:
            end_idx = min(start_idx + BLOCK_SIZE, len(self.signal)-1)
            self.current_sample = end_idx
        else:
            start_idx = min(end_idx - BLOCK_SIZE, 0)
            self.current_sample = start_idx

        return self.signal[start_idx:end_idx]
    
    # Get one second of signal, currently unused
    def get_second(self):
        start_idx = self.current_sample
        end_idx = self.current_sample

        if self.forward:
            end_idx = min(start_idx + self.current_fs, len(self.signal)-1)
            self.current_sample = end_idx + 1
        else:
            start_idx = min(end_idx - self.current_fs, 0)
            self.current_sample = start_idx - 1

        return self.signal[start_idx:end_idx]
    
    def resample(self, signal_in):
        return rs.resample(signal_in, self.current_fs)
    
    # Returns the signal to be played
    def play(self):
        if self.current_sample < 0 or self.current_sample >= len(self.signal):
            return
        
        # Take a block of signal and flip if going backwards
        
        signal_in = np.empty(BLOCK_SIZE)
        signal_out = []
        if self.forward:
            signal_in = self.get_block()
            return signal_in
        else:
            signal_in = self.get_block()
            signal_out = np.flip(signal_in)

        # Change sample rate if needed
        if self.signal_fs != self.current_fs:
           signal_out = self.resample(signal_out)

        return signal_out
    
            

        

    
