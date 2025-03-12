import tkinter as tk
from tkinter import ttk
import threading

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
        self.ot = threading.Thread(target=self.output_loop)
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
    
    def create_gui(self):
        self.root = tk.Tk()
        self.root.title('Button Demo')
        self.exit_button = ttk.Button(self.root, text='Exit', command=self.stop)
        self.playPause_button = ttk.Button(self.root,text='Play',command=self.playPause)
        self.exit_button.pack()
        self.playPause_button.pack()
        self.root.mainloop()
