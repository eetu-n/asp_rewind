from AudioOutput import AudioOutput
from gui import Player
import numpy as np

FS = 44100
BS = 1024
CHANNELS = 1

# For getting signal from Processor, recursive
# Not used yet
def play_processor(out, processor, player):
    signal_out = processor.play()
    if signal_out == []:
        player.stop()
        return
    
    if player.play:
        out.write(signal_out)

    if player.done:
        return
    
    output_loop(out, processor, player)   

length = 10
samples = np.linspace(0, length, int(FS*length))
signal = 0.5 * np.sin(2 * np.pi * 1000 * samples)

out = AudioOutput(FS, BS, CHANNELS)
player = Player(signal, out)

