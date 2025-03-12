import tkinter as tk
from tkinter import ttk
import numpy as np
import threading

from AudioOutput import AudioOutput

FS = 44100
BS = 1024
CHANNELS = 1

length = 10
samples = np.linspace(0, length, int(FS*length))
signal = 0.5 * np.sin(2 * np.pi * 1000 * samples)

class Player:
    def __init__(self, signal, output):
        self.signal = signal
        self.play = False
        self.stopped = False
        self.pressed = threading.Event()
        self.output = output
        self.ot = threading.Thread(target=self.output_loop)
        self.create_gui()
    
    def playPause(self):
        self.play = not self.play
        self.pressed.set()
    
    def stop(self):
        self.stopped = True
        self.pressed.set()
        #self.ot.join()
        self.root.quit()
        self.output.close()

    def output_loop(self):
        n = 0
        while n < len(self.signal):
            if not self.play:
                self.pressed.wait()
            if self.play:
                self.output.write(self.signal[n:n+self.output.block_length])
                n += self.output.block_length
            if self.stopped:
                break
            self.pressed.clear()
        self.stop()
    
    def create_gui(self):
        self.root = tk.Tk()
        self.root.title('Button Demo')
        self.exit_button = ttk.Button(self.root, text='Exit', command=self.stop)
        self.playPause_button = ttk.Button(self.root,text='Play',command=self.playPause)
        self.exit_button.pack()
        self.playPause_button.pack()
        self.ot.start()
        self.root.mainloop()

out = AudioOutput(FS, BS, CHANNELS)
player = Player(signal, out)
