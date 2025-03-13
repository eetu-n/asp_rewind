import tkinter as tk
from tkinter import ttk
import threading
import soundfile as sf
from processor import Processor

from AudioOutput import AudioOutput

FS = 48000
BS = 1024
CHANNELS = 1

length = 10
samples = np.linspace(0, length, int(FS*length))
signal = 0.5 * np.sin(2 * np.pi * 1000 * samples)

class Player:
    """
    Class for creating the player GUI, as well as handling commands for play, pause, rewind, fast-forward

    Arguments:
    signal:     The signal to play, see AudioOutput for format
    output:     An AudioOutput object for output
    enable_gui: Whether to draw the GUI

    Only functions that need be called by externals are playPause and stop.
    """
    def __init__(self, signal, output, enable_gui = True):
        self.signal = signal
        self.play = False
        self.stopped = False
        self.pressed = threading.Event()
        self.output = output
        self.ot = threading.Thread(target=self.play_makso)
        self.processor = Processor()
        self.create_gui()
        if enable_gui == True:
            self.create_gui()
        self.ot.start()
    
    def playPause(self):
        self.play = not self.play
        self.pressed.set()
    
    def stop(self):
        self.stopped = True
        self.pressed.set()
        self.ot.join()
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

    def play_makso(self):
        input, fs = sf.read("makso.wav")
        print(fs)

        if len(input.shape) > 1:  
            input = np.mean(input, axis=1)
        
        self.processor = Processor()
        self.processor.add_signal(input, fs)
        
        signal_out = self.processor.play()

        while not len(signal_out) == 0:
            if not self.play:
                self.pressed.wait()
            if self.play:
                self.output.write(signal_out)
            if self.stopped:
                break 
            signal_out = self.processor.play()
            #self.pressed().clear()
        self.stop()
    
    def create_gui(self):
        self.root = tk.Tk()
        self.root.title('Button Demo')
        self.exit_button = ttk.Button(self.root, text='Exit', command=self.stop)
        self.playPause_button = ttk.Button(self.root,text='Play',command=self.playPause)
        self.exit_button.pack()
        self.playPause_button.pack()
        self.root.mainloop()
