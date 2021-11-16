
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
from playerWin import PlayerWin

class CurrentGame(tk.Toplevel):


    def __init__(self,root):
        self.music_player = Player() 
        self.volume = 50
        shelveFile = shelve.open("shelveData", flag="r")
        self.player1Name = shelveFile["player1Name"]
        self.player2Name = shelveFile["player2Name"]
        self.clicksNumber = shelveFile["clicksNumber"]
        if "volume" in shelveFile:            
            self.volume = shelveFile["volume"]
        shelveFile.close()

        self.root = root


        self.countPressButton1 = 0
        self.countPressButton2 = 0

        super().__init__(root)
        self.initForm()
        self.title('Нажми на кнопку')
        self.wm_state('zoomed')
        self.resizable(0, 0) 
        self.attributes('-fullscreen', True)

    def initForm(self):


        self.btnCloseForm = tk.Button(self, text='Покинуть игру', command=self.destroy, background="black",
                                      foreground="white", font="Verdana 40 bold", width=12, borderwidth=2,
                                      relief='solid')
        self.btnCloseForm.pack(padx=10, pady=5, side=BOTTOM, fill=X)
        f1 = tk.Frame(self, bg='#E90000')
        f1.pack(side=LEFT, fill=BOTH, expand=1)
        l1 = Label(f1, width=100, height=1, bg='#E90000')
        l1.pack(fill=X)
        self.labelClicksNumberUser1 = tk.Label(f1, text=self.player1Name + '\n' + '0', fg='white', bg='#E90000', font="Verdana 40 bold", padx=0, pady=0)
        self.labelClicksNumberUser1.pack(expand=1)

        f2 = tk.Frame(self, bg='#10C5FF')
        f2.pack(side=LEFT, fill=BOTH, expand=1)

        l2 = Label(f2, width=100, height=1, bg='#10C5FF')
        l2.pack(fill=X)
        self.labelClicksNumberUser2 = tk.Label(f2, text=self.player2Name + '\n' + '0', fg='white', bg='#10C5FF', font="Verdana 40 bold", padx=0, pady=0)
        self.labelClicksNumberUser2.pack(expand=1)


        self.bind('1', self.player1btn)
        self.bind('2', self.player2btn)
        self.bind('<Escape>', self.closeForm)


        self.grab_set()
        self.focus_set()

    def player1btn(self, event):
        self.countPressButton1 = self.countPressButton1 + 1
        self.labelClicksNumberUser1.configure(text=self.player1Name + '\n' + str(self.countPressButton1))
        Thread(target=self.musicPlayer1, daemon=True).start()
        if int(self.countPressButton1) == int(self.clicksNumber):
            PlayerWin(self.root, self.player1Name, '1')
            self.destroy()


    def player2btn(self, event):
        self.countPressButton2 = self.countPressButton2 + 1
        self.labelClicksNumberUser2.configure(text=self.player2Name + '\n' + str(self.countPressButton2))
        Thread(target=self.musicPlayer2, daemon=True).start()
        if int(self.countPressButton2) == int(self.clicksNumber):
            PlayerWin(self.root, self.player2Name, '2')
            self.destroy()

    def musicPlayer1(self):
        song = pyglet.media.synthesis.Sawtooth(duration=0.08, frequency=350)
        self.music_player = Player()
        self.music_player.queue(song)
        self.music_player.volume = float(self.volume)/100.0
        self.music_player.play()

    def musicPlayer2(self):
        song = pyglet.media.synthesis.Sawtooth(duration=0.08, frequency=400)
        self.music_player = Player()
        self.music_player.queue(song)
        self.music_player.volume = float(self.volume)/100.0
        self.music_player.play()
        
    def closeForm(self, event):
        self.destroy()