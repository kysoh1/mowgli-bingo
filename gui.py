from tkinter import *
from PIL import ImageTk
from PIL import Image
import numpy as np

import platform

import bingo

class Application(Tk):
    def __init__(self):
        Tk.__init__(self)
        # Frame settings
        self.title("Welcome to Mowgli Bingo! Moooooooooowgli Edition")

        # Linux doesn't like calling this function. I mean if you think
        # about it Linux doesn't have icons for their apps anyways.
        curPlat = platform.system()
        if curPlat == "Windows":
            self.iconbitmap("Mowgli.ico")

        self.geometry("800x800")
        self.minsize(800, 700)
        self.maxsize(800, 700)
        
        # Store frames
        self.frames = {}
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        for frameType in (MainFrame, SettingsFrame):
            pageName = frameType.__name__
            frame = frameType(parent=container, app=self)
            self.frames[pageName] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.switchFrame(MainFrame.__name__)
        
    def switchFrame(self, frameType):
        frame = self.frames[frameType]
        frame.tkraise()
    

class MainFrame(Frame):
    def __init__(self, parent, app):
        Frame.__init__(self, parent)
        self.img = PhotoImage(file="Mowgli.png")
        self.label = Label(self, image=self.img)
        self.label.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.app = app
        self.game = bingo.Game(bingo.randomiseLabels())
        self.label = None
        self.createWidgets()
        
    def createWidgets(self):
        rowIdx = 0
        columnIdx = 0
        for row in self.game.labels:
            for label in row:
                button = Button(self, bg="#CCFFE5", activebackground="#CCFFE5", borderwidth=1, wraplength=100, justify=CENTER, text=label, font=("Arial", 10, "bold"), relief="flat", height=8, width=20)
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
            
        shuffleButton = Button(self, bg="#4F5F52", fg="white", activebackground="#4F5F52", activeforeground="white", borderwidth=0, text="Shuffle", font=("Helvetica", 10, "bold"), height=4, width=20, relief="solid", command=lambda: self.shuffleBingo())
        shuffleButton.place(x=100, y=600)
        labelButton = Button(self, bg="#4F5F52", fg="white", activebackground="#4F5F52", activeforeground="white", borderwidth=0, text="Change contents", font=("Helvetica", 10, "bold"), height=4, width=20, relief="solid", command=lambda: self.app.switchFrame(SettingsFrame.__name__))
        labelButton.place(x=550, y=600)
        
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
                self.label.place(x=330, y=600)
        elif self.label is not None:
            self.label.destroy()
            self.label = None
    
    def shuffleBingo(self):
        self.game = bingo.Game(bingo.randomiseLabels())
        self.createWidgets()

class SettingsFrame(Frame):
    def __init__(self, parent, app):
        Frame.__init__(self, parent)
        self.img = PhotoImage(file="Mowgli.png")
        self.label = Label(self, image=self.img)
        self.label.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.app = app
        self.createWidgets()
        
    def createWidgets(self):
        leaveButton = Button(self, text="Go back", height=5, width=20, command=lambda: self.app.switchFrame(MainFrame.__name__))
        leaveButton.place(x=0, y=0)
        leaveButton.pack()
        
