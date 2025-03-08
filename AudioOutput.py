import pyaudio
import numpy as np

class AudioOutput:
    def __init__(self, fs, chunk_size, channels):
        self.fs = fs
        self.chunk_size = chunk_size
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=channels,
            rate=self.fs,
            output=True,
            frames_per_buffer=self.chunk_size)
        self.stream.start_stream()

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
    
    def write(self, chunk):
        if len(chunk) > self.chunk_size:
            raise ValueError("Chunk length is " + len(chunk) + "\nShould be " + self.chunk_size)
        if type(chunk[0]) == np.float64:
            chunk = (chunk * 32767).astype(np.int16)
        self.stream.write(chunk.tobytes(), self.chunk_size)
