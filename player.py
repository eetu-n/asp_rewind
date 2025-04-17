import tkinter as tk
from tkinter import ttk
import threading
from processor import Processor
import numpy as np
import soundfile as sf

from audio_output import AudioOutput

import time

FS = 48000
BS = 1024
CHANNELS = 1

class Player:
    """
    Class for creating the player GUI, as well as handling commands for play, pause, rewind, fast-forward

    Arguments:
    signal:     The signal to play, see AudioOutput for format
    output:     An AudioOutput object for output
    enable_gui: Whether to draw the GUI

    Only functions that need be called by externals are playPause and stop.
    """
    def __init__(self, signal, output, enable_gui = True, fast_forward_speed = 2, ramp_time = 0.5):
        self.signal = signal
        self.play = False
        self.stopped = False
        self.pressed = threading.Event()
        self.output = output
        self.ramp = False
        self.flutter = False
        self.anti_alias = True
        self.smooth_change = True
        self.rewind_speed = -fast_forward_speed
        self.ff_speed = fast_forward_speed
        self.ramp_time = ramp_time
        self.ot = threading.Thread(target=self.output_loop)
        self.processor = Processor(signal, output.fs, output.block_size)
        self.ot.start()
        self.write_to_file = False
        self.played_data = []
        if enable_gui == True:
            self.create_gui()     
    
    def playPause(self):
        if self.play:
            target_speed = 0
        else:
            target_speed = 1
        self.processor.set_speed(target_speed, self.ramp, self.flutter, self.ramp_time)

        if self.ramp and self.play:
            time.sleep(self.ramp_time)

        self.play = not self.play

        # Change Button Text
        if not self.play:
            self.playPause_button.config(text="Play")
        else:
            self.playPause_button.config(text="Pause")

        self.pressed.set()
    
    def force_pause(self):
        self.processor.set_speed(0, ramp=False, flutter=False)
        self.play = False
        self.playPause_button.config(text="Play")
    
    def stop(self):
        self.stopped = True
        self.pressed.set()
        self.root.quit()
        self.output.close()

    def output_loop(self):
        while True:
            if not self.play:
                self.pressed.wait()
            if self.play:
                try:
                    signal_out = self.processor.play(anti_alias = self.anti_alias, smooth_changes = self.smooth_change)
                except EOFError:
                    print("No data to play!")
                    self.force_pause()
                    self.pressed.clear()
                    continue
                else:
                    self.output.write(signal_out)
            if self.stopped:
                break 
            if self.write_to_file:
                self.played_data = np.append(self.played_data, signal_out)
            self.pressed.clear()
        self.stop()
    
    def rewind(self):
        self.processor.set_speed(self.rewind_speed, self.ramp, self.flutter, self.ramp_time)
        self.playPause_button.config(text="Pause")
        self.play = True
        self.pressed.set()
    
    def fast_forward(self):
        self.processor.set_speed(self.ff_speed, self.ramp, self.flutter, self.ramp_time)
        self.playPause_button.config(text="Pause")
        self.play = True
        self.pressed.set()

    def save_file(self):
        if self.write_to_file:
            print(len(self.played_data))
            sf.write("./audio/output.wav", self.played_data, self.output.fs)
            self.played_data = []
            self.write_to_file = False
        else:
            self.write_to_file = True
    
    def ramp_toggle(self):
        self.ramp = not self.ramp
        if self.ramp:
            self.ramp_button.config(text="Ramp Off")
        else:
            self.ramp_button.config(text="Ramp On")

    def flutter_toggle(self):
        self.flutter = not self.flutter
        if self.flutter:
            self.flutter_button.config(text="Flutter Off")
        else:
            self.flutter_button.config(text="Flutter On")

    def anti_alias_toggle(self):
        self.anti_alias = not self.anti_alias
        if self.anti_alias:
            self.anti_alias_button.config(text="Anti-Alias Off")
        else:
            self.anti_alias_button.config(text="Anti-Alias On")

    def smooth_change_toggle(self):
        self.smooth_change = not self.smooth_change
        if self.smooth_change:
            self.smooth_change_button.config(text="Smooth Changes Off")
        else:
            self.smooth_change_button.config(text="Smooth Changes On")
    
    def create_gui(self):
        self.root = tk.Tk()
        self.root.title('Fast Forward / Rewind Demo')
        self.root.geometry("400x100")

        self.exit_button = ttk.Button(self.root, text='Exit', command=self.stop)
        self.exit_button.pack(side=tk.BOTTOM)

        self.save_button = ttk.Button(self.root,text='Write to file',command=self.save_file)
        self.save_button.pack(side=tk.BOTTOM)

        self.playPause_button = ttk.Button(self.root,text='Play',command=self.playPause)
        self.playPause_button.pack(side=tk.RIGHT)

        self.rewind_button = ttk.Button(self.root,text='Rewind',command=self.rewind)
        self.rewind_button.pack(side=tk.RIGHT)

        self.ff_button = ttk.Button(self.root,text='Fast Forward',command=self.fast_forward)
        self.ff_button.pack(side=tk.RIGHT)

        self.ramp_button = ttk.Button(self.root,text='Ramp On',command=self.ramp_toggle)
        self.ramp_button.pack(side=tk.LEFT)

        self.flutter_button = ttk.Button(self.root,text='Flutter On',command=self.flutter_toggle)
        self.flutter_button.pack(side=tk.LEFT)

        self.anti_alias_button = ttk.Button(self.root,text='Anti-Alias Off',command=self.anti_alias_toggle)
        self.anti_alias_button.pack(side=tk.LEFT)

        self.smooth_change_button = ttk.Button(self.root,text='Smooth Changes Off',command=self.smooth_change_toggle)
        self.smooth_change_button.pack(side=tk.LEFT)

        #slider = ttk.Scale(root, from_=0, to=100, orient='horizontal', variable = )

        self.exit_button.pack()
        self.playPause_button.pack()
        self.rewind_button.pack()
        self.ff_button.pack()
        self.ramp_button.pack()

        self.root.wm_attributes("-type", "dialog")

        self.root.mainloop()
