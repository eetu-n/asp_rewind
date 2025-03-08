from AudioOutput import AudioOutput
import numpy as np

import threading

BLOCK_LENGTH = 1024
fs = 44100

def input_loop(player):
    while not player.done:
        inp = input("Input:")
        if inp == 's':
            player.finish()
        if inp == 'l':
            player.start()
        if inp == 'a':
            player.stop()

def output_loop(out, data, player):
    n = 0
    while n < len(data):
        if player.play:
            out.write(data[n:n+BLOCK_LENGTH])
            n += BLOCK_LENGTH
        if player.done:
            break

class Player:
    def __init__(self):
        self.play = False
        self.done = False
    
    def start(self):
        self.play = True
    
    def stop(self):
        self.play = False
    
    def finish(self):
        self.done = True

player = Player()

length = 10
samples = np.linspace(0, length, int(fs*length))
signal = 0.5 * np.sin(2 * np.pi * 1000 * samples)

out = AudioOutput(fs, BLOCK_LENGTH, 1)

t2 = threading.Thread(target=output_loop, args=(out, signal, player))
t2.start()

t1 = threading.Thread(target=input_loop, args=(player,))
t1.start()

t1.join()
t2.join()

out.close()
