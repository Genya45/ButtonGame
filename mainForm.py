
from currentGame import CurrentGame
from intermediateGame import IntermediateGame
import shelve
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
from threading import Thread
from playsound import playsound
from pyglet.resource import media
from pyglet.media import Player
from playsound import playsound
import pyglet




class Main(tk.Frame):

    def __init__(self, root):

        self.userName1 = tk.StringVar()
        self.userName2 = tk.StringVar()
        self.clicksNumber = tk.StringVar()

        self.volume = 50
        self.userName1DB = "Имя 1"
        self.userName2DB = "Имя 2"
        self.userClicksDB = "50"

        try:
            file = open('shelveData.dat')
        except IOError as e:
            shelveFile = shelve.open("shelveData", flag="n")
            shelveFile.close()
        else:
            with file:
                shelveFile = shelve.open("shelveData", flag="r")
                if "volume" in shelveFile:            
                    self.volume = shelveFile["volume"]
                if "player1Name" in shelveFile:            
                    self.userName1DB = shelveFile["player1Name"]
                if "player2Name" in shelveFile:            
                    self.userName2DB = shelveFile["player2Name"]
                if "clicksNumber" in shelveFile:            
                    self.userClicksDB = shelveFile["clicksNumber"]
                shelveFile.close()


        



        super().__init__(root)
        root.title("Игра в кнопки")
        root.resizable(0, 0)
        root.attributes('-fullscreen', True)
        root.wm_state('zoomed')
        
        self.music_player = Player()

        root.resizable(False, False)
        self.init_main()



    def init_main(self):

        Thread(target=self.musicPlay, daemon=True).start()
        self.musicPlay()

        self.btnCloseForm = tk.Button(self, text='Покинуть игру', command=root.destroy, background="black",
                                      foreground="white", font="Verdana 40 bold", width=12, borderwidth=2,
                                      relief='solid')
        self.btnCloseForm.pack(padx=10, pady=10, side=BOTTOM, fill=X)

        self.labelVolume = tk.Label(root, text='Громкость', fg='black', font="Verdana 10 bold")
        self.labelVolume.pack(side=BOTTOM, fill=X)
        self.scal = tk.Scale(root,orient=HORIZONTAL,length=300,from_=0,to=100,tickinterval=10,resolution=5)
        self.scal.pack(side=BOTTOM, fill=X)
        self.scal.set(self.volume)
        self.scal.bind("<B1-Motion>",self.get_val_motion)

        f1 = tk.Frame(root)
        f2 = LabelFrame(f1)
        f3 = LabelFrame(f1)

        self.labelPlayer1Name = tk.Label(f2, text='Игрок 1', fg='black', font="Impacted 40")
        self.labelPlayer1Name.pack(padx=20, pady=20)
        self.entryPlayer1Name = ttk.Entry(f2, width=23, textvariable=self.userName1, justify='center', font="Impacted 30 italic")
        self.entryPlayer1Name.pack(padx=20, pady=20)

        self.labelPlayer2Name = tk.Label(f3, text='Игрок 2', fg='black', font="Impacted 40")
        self.labelPlayer2Name.pack(padx=20, pady=20)
        self.entryPlayer2Name = ttk.Entry(f3, width=23, textvariable=self.userName2, justify='center', font="Impacted 30 italic")
        self.entryPlayer2Name.pack(padx=20, pady=20)

        self.entryPlayer1Name.insert(0, self.userName1DB)
        self.entryPlayer2Name.insert(0, self.userName2DB)

        f1.pack(side=TOP)
        f2.pack(side=LEFT, padx=20, pady=20, fill=Y)
        f3.pack(side=RIGHT, padx=20, pady=20, fill=Y)


        fClicksNumber = tk.Frame(root)

        self.labelClicksNumber = tk.Label(fClicksNumber, text='Количество нажатий', fg='black', font="Verdana 40 bold")
        self.labelClicksNumber.pack(padx=20, pady=20, side=LEFT)
        self.entryClicksNumber = ttk.Entry(fClicksNumber, width=23, textvariable=self.clicksNumber, justify='center', font="Impacted 30 italic")
        self.entryClicksNumber.pack(padx=20, pady=20, side=LEFT)

        self.entryClicksNumber.insert(0, self.userClicksDB)

        fClicksNumber.pack()


        fBtn = tk.Frame(root)

        self.btnStartGame = tk.Button(fBtn, text='Кто быстрее?', command=self.initGameForm, background="#10C5FF", foreground="white", font="Verdana 40 bold", width=12, borderwidth=2, relief='solid')
        self.btnStartGame.pack(padx=50, pady=20, side=LEFT)
        self.btnStartGameFirstPress = tk.Button(fBtn, text='Кто первый?', command=self.initGameFormFirstPress, background="#E90000", foreground="white", font="Verdana 40 bold", width=12, borderwidth=2, relief='solid')
        self.btnStartGameFirstPress.pack(padx=50, pady=20, side=LEFT)

        fBtn.pack(side=TOP)

        
    def get_val_motion(self, event):
        shelveFile = shelve.open("shelveData", flag="n")
        shelveFile["volume"] = str(self.scal.get())
        shelveFile.close()

    def initGameForm(self):

        if str(self.entryPlayer1Name.get()) == '' or str(self.entryPlayer2Name.get()) == '' or str(self.entryClicksNumber.get()) == '':
            messagebox.showinfo('Ошибка', 'Заполните пустые поля')
            return
        if self.entryClicksNumber.get().isdigit() == False:
            messagebox.showinfo('Ошибка', 'Введите только цифры в поле количества нажатий')
            return
        if int(self.entryClicksNumber.get()) < 1:            
            messagebox.showinfo('Ошибка', 'Некоректное количество нажатий')
            return

        shelveFile = shelve.open("shelveData", flag="n")
        shelveFile["player1Name"] = str(self.entryPlayer1Name.get())
        shelveFile["player2Name"] = str(self.entryPlayer2Name.get())
        shelveFile["clicksNumber"] = str(self.entryClicksNumber.get())
        shelveFile["volume"] = str(self.scal.get())
        shelveFile.close()

        IntermediateGame(root,1)

    def initGameFormFirstPress(self):

        if str(self.entryPlayer1Name.get()) == '' or str(self.entryPlayer2Name.get()) == '':
            messagebox.showinfo('Ошибка', 'Заполните пустые поля')
            return

        shelveFile = shelve.open("shelveData", flag="n")
        shelveFile["player1Name"] = str(self.entryPlayer1Name.get())
        shelveFile["player2Name"] = str(self.entryPlayer2Name.get())
        shelveFile["clicksNumber"] = str(self.entryClicksNumber.get())
        shelveFile["volume"] = str(self.scal.get())
        shelveFile.close()

        IntermediateGame(root,2)

    def musicPlay(self):
        #song = pyglet.media.synthesis.Sawtooth(duration=0.1, frequency=400)
        #song.play()       
        song = pyglet.media.synthesis.Sawtooth(duration=0.1, frequency=400)
        self.music_player.queue(song)
        self.music_player.volume = 0.04
        self.music_player.play()




if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    app.pack()
    root.mainloop()
