
import tkinter as tk
import shelve
import pyglet
from tkinter import *
from currentGame import CurrentGame
from firstPressGame import FirstPressGame
from threading import Thread
from pyglet.resource import media
from pyglet.media import Player
from playsound import playsound

class IntermediateGame(tk.Toplevel):


    def __init__(self, root, mode):
        self.volume = 50        
        shelveFile = shelve.open("shelveData", flag="r")
        if "volume" in shelveFile:            
            self.volume = shelveFile["volume"]
        self.music_player = Player()
        self.frequency = 400
        self.mode = mode
        self.root = root
        self.sec = 0
        super().__init__(root)
        self.initForm()
        self.title('Скоро игра!!!')
        self.wm_state('zoomed')
        self.resizable(0, 0)
        self.attributes('-fullscreen', True)
        self.tick()



    def initForm(self):
        
        self.time = Label(self, fg='#E90000', font="Verdana 250 bold")
        self.time.pack(expand=1, fill=BOTH, side=BOTTOM)
        self.l = Label(self, text='Игра начнеться через', font="Verdana 70 bold", fg='#10C5FF')
        self.l.pack(side=TOP)

        self.grab_set()
        self.focus_set()


    def tick(self):
        self.sec += 1
        self.time['text'] = 6 - self.sec
        self.frequency = self.frequency + 150
        
        Thread(target=self.musicPlay, daemon=True).start()
        if self.sec < 6:
            self.time.after(1000, self.tick)
            
        if self.sec >= 6:
            if self.mode == 1:
                CurrentGame(self.root)
            else:
                FirstPressGame(self.root)
            self.destroy()
        
    def musicPlay(self):
        song = pyglet.media.synthesis.Sawtooth(duration=0.4, frequency=self.frequency)        
        self.music_player = Player()
        self.music_player.queue(song)
        self.music_player.volume = float(self.volume)/100.0
        self.music_player.play()


