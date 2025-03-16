import numpy as np
import scipy.signal as sig
import soundfile as sf
from matplotlib import pyplot as plt
from resampy import resample
from speed import speed_function
from math import ceil

EFFECT_DURATION = 4*430 # blocks, approx 10 seconds

class Processor():
    def __init__(self, signal = [0], fs = 48000, block_size=512):
        self.forward = True
        self.current_sample = 0
        self.upcoming_ratio = []
        self.signal = []
        self.block_size = block_size
        self.prev_ratio = 0
        self.add_signal(signal, fs)
        
    def add_signal(self, signal_in, fs):
        # Which one?
        #self.signal = np.concatenate([self.signal, signal_in],0)
        self.signal = np.append(self.signal, signal_in)
        self.signal_fs = fs
        self.current_ratio = 0

        # FOR TESTING PURPOSES:
        #self.forward = False
        #self.current_sample = len(self.signal)-1
        #self.current_ratio = -1
        #self.upcoming_ratio = []
        #self.set_speed()

    # (useless for now)
    def change_rate(self, ratio):
        self.current_ratio = ratio
        if ratio > 0:
            self.forward = True
        else:
            self.forward = False

    def update_rate(self):
        # Back to original speed if no upcoming ratio
        if len(self.upcoming_ratio) == 0:
            #self.current_ratio = 1
            return 
        
        # Update from upcoming ratios
        self.prev_ratio = self.current_ratio
        self.current_ratio = self.upcoming_ratio[0]
        del self.upcoming_ratio[0]
        
        # Update direction
        if self.current_ratio > 0:
            self.forward = True
        else:
            self.forward = False

    def get_input_sample_number(self):
        return int(abs(self.current_ratio) * self.block_size)

    # Get one block of signal
    def get_block(self):
        start_idx = self.current_sample
        end_idx = self.current_sample

        num_samples = self.get_input_sample_number()
        
        # Update start and end indices      
        if self.forward:
            end_idx = min(start_idx + num_samples, len(self.signal)-1)
            self.current_sample = end_idx
        else:
            start_idx = max(end_idx - num_samples, 0)
            self.current_sample = start_idx

        return self.signal[start_idx:end_idx]

    def resample(self, signal_in, start_speed, end_speed):
        num_samples = len(signal_in)
        
        time_original = np.linspace(0, num_samples, num_samples)

        if start_speed == end_speed:
            return resample(signal_in, self.signal_fs, abs(int(self.signal_fs/self.current_ratio)))

        playback_speed_curve = np.linspace(end_speed, start_speed, self.block_size)

        time_warped = np.cumsum(1 / playback_speed_curve)
        #time_warped = time_warped / time_warped[-1] * (num_samples - 1)
        time_warped = (time_warped - time_warped[0]) / (time_warped[-1] - time_warped[0]) * (num_samples - 1)

        return np.interp(time_warped, time_original, signal_in)
    
    def set_speed(self, ratio = 1, ramp = False, flutter = False, ramp_time = 0.5):
        ramp_blocks = int(ceil((ramp_time * self.signal_fs) / self.block_size))

        speed = speed_function(ratio, ramp, flutter, self.current_ratio, ramp_blocks = ramp_blocks, block_size = self.block_size)
        self.upcoming_ratio = speed.tolist()
   
    # Returns the signal to be played (1024 samples)
    def play(self):
        # Check that there is signal to play, else return
        if self.current_sample < 0 or self.current_sample >= len(self.signal):
            print("No signal left to play")
            return []
        
        # Update sampling rate
        self.update_rate()

        signal_in = self.get_block()
        #print("Signal in before resample: ", len(signal_in))
        signal_out = np.zeros(self.block_size) # Fixed size

        # Flip signal if going backwards
        if not self.forward:
            signal_in = np.flip(signal_in)

        # Change sample rate if needed
        if abs(self.current_ratio) != 1:
            if len(self.upcoming_ratio) != 0:
                signal_in = self.resample(signal_in, self.prev_ratio, self.current_ratio)
            else:
                signal_in = self.resample(signal_in, self.current_ratio, self.current_ratio)


        #print("Signal in after resample: ", len(signal_in))

        # Pad with zeros if ran out of signal
        if len(signal_in) == self.block_size:
            return signal_in

        signal_out[0:len(signal_in)] = signal_in[0:min(len(signal_in), self.block_size)]

        return signal_out
