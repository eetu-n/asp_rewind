import numpy as np
import scipy.io.wavfile as wav
import soundfile as sf
from matplotlib import pyplot as plt
import resampy

def normalize_audio(data):
    """ Normalize audio to the range [-1, 1] """
    return data / np.max(np.abs(data))

def process(block):
    """ Takes one block of the signal to be processed """
    #block = normalize_audio(block)
    return block

def backwards(signal_in):
    """ Plays given signal backwards """
    signal_out = np.empty(len(signal_in))

    signal_out = np.flip(signal_in)

    return signal_out

    sample_idx = len(signal_in)-1
    for sample in signal_in:
        signal_out[sample_idx] = sample
        sample_idx -= 1

    return signal_out

def process_blocks(signal_in):
    """ Process input in blocks """
    
    block_size = 1024*10
    num_samples = len(signal_in)
    num_blocks = round(num_samples/block_size)
    
    #signal_out = np.empty(len(signal_in))
    signal_out = []

    first_time = True
    forward = True
    block_idx = 0
    
    while block_idx < num_blocks:
        start_idx = block_idx * block_size
        end_idx = min(start_idx + block_size-1, num_samples-1)

        signal_block = signal_in[start_idx:end_idx]

        #signal_out[start_idx:end_idx] = process(signal_block)
        
        if block_idx == 50 and first_time:
            forward = False
            first_time = False
        elif block_idx == 0:
            forward = True

        if forward:
            signal_out = np.concatenate((signal_out, signal_block),0)
            block_idx += 1
        else:
            signal_out = np.concatenate((signal_out, backwards(signal_block)),0)
            block_idx -= 1
 

    return signal_out

input, fs = sf.read("makso.wav", dtype='float32')
#plt.plot(input[:,0])
#plt.show()

print(input)
if len(input.shape) > 1:  
    input = np.mean(input, axis=1)
output = process_blocks(input)

sf.write("makso_backwards.wav", output, fs)
print("done")