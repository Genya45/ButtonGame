
import shelve
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from threading import Thread
from playsound import playsound
import pyglet
from pyglet.resource import media
from pyglet.media import Player
from tkinter import *

class PlayerWin(tk.Toplevel):


    def __init__(self,root, userName, colorMode):
        self.root = root
        self.volume = 50        
        shelveFile = shelve.open("shelveData", flag="r")
        if "volume" in shelveFile:            
            self.volume = shelveFile["volume"]
        self.userName = userName
        if colorMode == "1":
            self.colorWin = "#E90000"
            self.colorBtn = "#10C5FF"
        else:
            self.colorWin = "#10C5FF"
            self.colorBtn = "#E90000"

        self.music_player = Player()

        super().__init__(root)
        self.initForm()
        self.title('Победа!!!')
        self.wm_state('zoomed')
        self.resizable(0, 0)
        self.attributes('-toolwindow', True)
        self.attributes('-fullscreen', True)
        Thread(target=self.musicPlay, daemon=True).start()

    def initForm(self):


        self.bind('<space>', self.restartGame)
        self.bind('<Escape>', self.closeForm)

        l = Label(self, bg=self.colorWin, text='Победил\n' + self.userName, font="Verdana 70 bold", fg='white')
        l.pack(expand=1, fill=BOTH)

        self.btnCloseForm = tk.Button(self, text='Покинуть игру', command=self.destroy, background="black",
                                      foreground="white", font="Verdana 30 bold", width=12, borderwidth=2,
                                      relief='solid')
        self.btnCloseForm.pack(padx=2, pady=2, side=BOTTOM, fill=X)
        
        self.btnRestartGame = tk.Button(self, text='Переиграть', command=self.destroy, background=self.colorBtn,
                                      foreground="white", font="Verdana 30 bold", width=12, borderwidth=2,
                                      relief='solid')
        self.btnRestartGame.pack(padx=2, pady=2, side=BOTTOM, fill=X)

        self.grab_set()
        self.focus_set()

    def musicPlay(self):
        song = pyglet.media.synthesis.Sawtooth(duration=0.5, frequency=600)
        self.music_player = Player()
        self.music_player.queue(song)
        self.music_player.volume = float(self.volume)/100.0
        self.music_player.play()

    def restartGame(self, event):
        from intermediateGame import IntermediateGame
        IntermediateGame(self.root,1)
        self.destroy()

    def closeForm(self, event):
        self.destroy()