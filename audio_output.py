import pyaudio
import numpy as np

class AudioOutput:
    def __init__(self, fs, block_length, channels):
        self.fs = fs
        self.block_length = block_length
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=channels,
            rate=self.fs,
            output=True,
            frames_per_buffer=self.block_length)
        self.stream.start_stream()

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
    
    def write(self, block):
        if len(block) > self.block_length:
            raise ValueError("Provided block is of length " + len(block) + "\nShould be <= " + self.block_length)
        if type(block[0]) == np.float64:
            block = (block * 32767).astype(np.int16)
        self.stream.write(block.tobytes(), self.block_length)
