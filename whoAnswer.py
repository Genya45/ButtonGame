
import shelve
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from threading import Thread
from playsound import playsound
import pyglet
from tkinter import *

class WhoAnswer(tk.Toplevel):


    def __init__(self,root, text, mode, color):
        self.text = text
        self.mode = mode
        self.color = color

        super().__init__(root)
        self.initForm()
        self.title('Победа!!!')
        self.wm_state('zoomed')
        self.resizable(0, 0)
        self.attributes('-fullscreen', True)



    def initForm(self):
        self.btnCloseForm = tk.Button(self, text='Покинуть игру', command=self.destroy, background="black",
                                      foreground="white", font="Verdana 40 bold", width=12, borderwidth=2,
                                      relief='solid')
        self.btnCloseForm.pack(padx=10, pady=5, side=BOTTOM, fill=X)

        l = Label(self,bg=self.color, text=self.text, font="Verdana 70 bold", fg='white')
        l.pack(expand=1, fill=BOTH)

        self.bind('1', self.player1btn)
        self.bind('2', self.player2btn)
        self.bind('<Escape>', self.closeForm)


        self.grab_set()
        self.focus_set()

    def player1btn(self, event):
        if self.mode == '1':
            self.destroy()


    def player2btn(self, event):
        if self.mode == '2':
            self.destroy()

    def closeForm(self, event):
        self.destroy()