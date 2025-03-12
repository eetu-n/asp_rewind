import numpy as np
import scipy.io.wavfile as wav
import soundfile as sf
from matplotlib import pyplot as plt
import resampy as rs
from speed import speed_function

OUT_BLOCK_SIZE = 1024
EFFECT_DURATION = 10

class Processor():
    def __init__(self):
        self.signal = []
        self.forward = True
        self.current_sample = 0
        self.signal_fs = 0
        self.current_ratio = 0
        self.upcoming_ratio = []
        
    def add_signal(self, signal_in, fs):
        # Which one?
        #self.signal = np.concatenate([self.signal, signal_in],0)
        self.signal = np.append(self.signal, signal_in)
        self.signal_fs = fs
        self.current_ratio = 1

    def change_rate(self, ratio):
        self.current_ratio = ratio
        if ratio > 0:
            self.forward = True
        else:
            self.forward = False

    def update_rate(self):
        if len(self.upcoming_ratio) == 0:
            return 
        
        self.current_ratio = self.upcoming_ratio[0]
        self.upcoming_ratio = self.upcoming_ratio[1:]
        
        if self.current_ratio > 0:
            self.forward = True
        else:
            self.forward = False

    def get_input_sample_number(self):
        return round(abs(self.current_ratio) * OUT_BLOCK_SIZE)

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
        return rs.resample(signal_in, self.ratio*self.signal_fs)
    
    def set_speed(self, type="constant", ratio=2):
        time = np.linspace(0, EFFECT_DURATION*OUT_BLOCK_SIZE, self.signal_fs)
        speed = speed_function(time, type, ratio)
        ## Something to translate speed func to block fs?
        self.upcoming_ratio = speed
   
    # Returns the signal to be played (1024 samples)
    def play(self):
        # Check that there is signal to play, else return
        if self.current_sample < 0 or self.current_sample >= len(self.signal):
            print("No signal left to play")
            return []
        
        # Update sampling rate
        #self.update_rate()

        signal_in = self.get_block()
        signal_out = np.zeros(OUT_BLOCK_SIZE) # Fixed size

        print(signal_in)

        # Flip signal if going backwards
        if not self.forward:
            signal_in = np.flip(signal_in)

        print(signal_in)

        # Change sample rate if needed
        if abs(self.current_ratio) != 1:
           signal_in = self.resample(signal_in)

        print(signal_in)


        # Pad with zeros if ran out of signal
        signal_out[0:len(signal_in)] = signal_in

        return signal_out
    
            

        

    
