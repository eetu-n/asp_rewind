import pyaudio
import numpy as np

class AudioOutput:
    """
    Class for audio output.

    Arguments:
    fs:         Output sampling frequency
    block_size: Output block size
    channels:   Number of output channels
    """
    def __init__(self, fs, block_size, channels):
        self.fs = fs
        self.block_size = block_size
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=channels,
            rate=self.fs,
            output=True,
            frames_per_buffer=self.block_size)
        self.stream.start_stream()

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
    
    def write(self, block):
        """
        Write a block of audio into the output device

        Arguments:
        block:  The audio to write, either in np.int16 or np.float64
        """
        if len(block) > self.block_size:
            raise ValueError("Provided block is of length " + len(block) + "\nShould be <= " + self.block_size)
        if type(block[0]) == np.float64:
            block = (block * 32767).astype(np.int16)
        self.stream.write(block.tobytes(), self.block_size)
