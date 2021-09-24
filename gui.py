from tkinter import *
from PIL import ImageTk
from PIL import Image
from playsound import playsound
import multiprocessing
import platform
import numpy as np

if platform.system() == "Windows":
    import winsound

import bingo

class Application(Tk):
    def __init__(self):
        Tk.__init__(self)
        #Frame settings
        self.title("Welcome to Mowgli Bingo! Moooooooooowgli Edition")
        
        # Long story short, Linux systems don't really have icons on their windows.
        if platform.system() == "Windows":
        	self.iconbitmap("Mowgli.ico")
        	
        self.geometry("800x800")
        self.minsize(800, 700)
        self.maxsize(800, 700)
        
        #Game object
        self.game = bingo.Game()
        
        #Store frames
        self.frames = {}
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        for frameType in (MainFrame, SettingsFrame):
            pageName = frameType.__name__
            frame = frameType(parent=container, app=self, game=self.game)
            self.frames[pageName] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.switchFrame(MainFrame.__name__)
        
    def switchFrame(self, frameType):
        frame = self.frames[frameType]
        frame.tkraise()

class MainFrame(Frame):
    def __init__(self, parent, app, game):
        Frame.__init__(self, parent)
        self.img = PhotoImage(file="Mowgli.png")
        self.label = Label(self, image=self.img)
        self.label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Essentially this is a background process that will run. It will call the playsound
        # function to play BN.
        self.p = multiprocessing.Process(target=playsound, args=("TheBareNecessities.wav",))
        
        self.app = app
        self.game = game
        self.label = None
        self.shuffleBingo()
        self.createWidgets()
        
    # We are essentially overriding the inherited function.
    def destroy(self):
        # When the frame is destroyed we do not want the music to continue playing.
        if self.p.is_alive():
            self.p.terminate()
            self.p = multiprocessing.Process(target=playsound, args=("TheBareNecessities.wav",))
            
        Frame.destroy(self)
    
    def createWidgets(self):
        rowIdx = 0
        columnIdx = 0
        for row in self.game.labels:
            for label in row:
                button = Button(self, bg="#CCFFE5", activebackground="#D2FF4D", borderwidth=1, wraplength=100, justify=CENTER,
                                text=label, font=("Arial", 10, "bold"), relief="flat", cursor="hand2", height=8, width=20)
                button.configure(command=lambda button=button, x=columnIdx, y=rowIdx: self.buttonClick(button, x, y))
                #Pad top left
                if columnIdx == 0 and rowIdx == 0:
                    button.grid(row=rowIdx, column=columnIdx, padx=(60, 0), pady=(30, 0))
                #Pad left side of grid
                elif columnIdx == 0:
                    button.grid(row=rowIdx, column=columnIdx, padx=(60, 0))
                #Pad top side of grid
                elif rowIdx == 0:
                    button.grid(row=rowIdx, column=columnIdx, pady=(30, 0))
                else:
                    button.grid(row=rowIdx, column=columnIdx)
                
                columnIdx = columnIdx + 1
                
            rowIdx = rowIdx + 1
            columnIdx = 0
            
        shuffleButton = Button(self, bg="#4F5F52", fg="white", activebackground="#669900", activeforeground="white",
                               borderwidth=0, text="Shuffle", font=("Helvetica", 10, "bold"), cursor="hand2", height=4, width=20,
                               relief="solid", command=lambda: self.shuffleBingo())
        shuffleButton.place(x=60, y=615)
        
        labelButton = Button(self, bg="#4F5F52", fg="white", activebackground="#669900", activeforeground="white",
                             borderwidth=0, text="Change contents", font=("Helvetica", 10, "bold"), cursor="hand2", height=4, width=20,
                             relief="solid", command=lambda: self.app.switchFrame(SettingsFrame.__name__))
        labelButton.place(x=566, y=615)
        
    def buttonClick(self, button, x, y):
        state = self.game.state
        self.game.updateState(y, x)
        if state[y][x] == 1:
            button.configure(bg="#00FF80")
        else:
            button.configure(bg="#CCFFE5")
            
        if self.game.checkWin():
            if self.label is None:
                self.label = Label(self, text="Bingo!", height=5, width=20)
                
                # If it is Windows we must use winsound to play the audio.
                if platform.system() == "Windows":
                    winsound.PlaySound("TheBareNecessities.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
                else:
                    self.p.start()
                
                self.label.place(x=330, y=600)
        elif self.label is not None:
            self.label.destroy()
            
            if platform.system() == "Windows":
                winsound.PlaySound(None, winsound.SND_FILENAME)
                
            if self.p.is_alive():
                self.p.terminate()
                self.p = multiprocessing.Process(target=playsound, args=("TheBareNecessities.wav",))
                 
            self.label = None
    
    def shuffleBingo(self):
        self.game.randomiseLabels()
        self.game.resetState()
        self.createWidgets()
        
        # When the shuffle button is pressed we do not want the music to continue playing.
        if self.p.is_alive():
            self.p.terminate()
            self.p = multiprocessing.Process(target=playsound, args=("TheBareNecessities.wav",))

        # When the shuffle button is pressed kill the playing sound on a Windows machine.
        if platform.system() == "Windows":
            winsound.PlaySound(None, winsound.SND_FILENAME)
        
        if self.label is not None:
            self.label.destroy()
            self.label = None

class SettingsFrame(Frame):
    def __init__(self, parent, app, game):
        Frame.__init__(self, parent)
        self.img = PhotoImage(file="Mowgli.png")
        self.label = Label(self, image=self.img)
        self.label.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.app = app
        self.game = game
        self.texts = []
        self.createWidgets()
        
    def createWidgets(self):
        labels = np.array(self.game.labels).ravel().tolist()
        for i in range(0, len(labels) // 2):
            leftText = Text(self, bg="#CCFFE5", borderwidth=2, height=4, width=40, relief="solid")
            rightText = Text(self, bg="#CCFFE5", borderwidth=2, height=4, width=40, relief="solid")
            leftText.insert(INSERT, labels[i])
            rightText.insert(INSERT, labels[i + len(labels) // 2])
            
            if i == 0:
                leftText.grid(row=i, column=0, padx=(80, 20), pady=(10, 1))
                rightText.grid(row=i, column=1, pady=(10, 1))
            else:
                leftText.grid(row=i, column=0, padx=(80, 20), pady=(1, 1))
                rightText.grid(row=i, column=1, pady=(1, 1))
            
            self.texts.append(leftText)
            self.texts.append(rightText)
            
        saveButton = Button(self, bg="#4F5F52", fg="white", activebackground="#4F5F52", activeforeground="white",
                            borderwidth=0, text="Save settings", font=("Helvetica", 10, "bold"), height=4, width=25,
                            command=lambda: self.saveSettings())
        saveButton.place(x=130, y=600)
        leaveButton = Button(self, bg="#4F5F52", fg="white", activebackground="#4F5F52", activeforeground="white",
                             borderwidth=0, text="Go back", font=("Helvetica", 10, "bold"), height=4, width=25,
                             command=lambda: self.app.switchFrame(MainFrame.__name__))
        leaveButton.place(x=500, y=600)
    
    def saveSettings(self):
        newLabels = []
        for text in self.texts:
            label = text.get(1.0, END).strip("\n")
            newLabels.append(label)
        
        newLabels = np.array(newLabels).reshape(4, 4)
        self.game.changeLabels(newLabels.tolist())
