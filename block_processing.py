import numpy as np
import scipy.io.wavfile as wav
import resampy

def normalize_audio(data):
    """ Normalize audio to the range [-1, 1] """
    return data / np.max(np.abs(data))

def process(block):
    """ Takes one block of the signal to be processed """

def process_blocks(signal_in):
    """ Process input in blocks """
    
    block_size = 1024
    num_samples = len(signal_in)
    num_blocks = round(num_samples/block_size)

    block_idx = 0
    while block_idx < num_blocks:
        start_idx = block_idx * block_size
        end_idx = min(start_idx + block_size-1, num_samples-1)

        signal_block = signal_in[start_idx:end_idx]

        process(signal_block)

        block_idx += 1
        print(block_idx)

    
