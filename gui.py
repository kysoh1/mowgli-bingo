from tkinter import *
from PIL import ImageTk
from PIL import Image
import numpy as np

import bingo

class Application(Tk):
    def __init__(self):
        Tk.__init__(self)
        #Frame settings
        self.title("Welcome to Mowgli Bingo! Moooooooooowgli Edition")
        self.iconbitmap("Images/Mowgli.ico")
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
        self.img = PhotoImage(file="Images/Mowgli.png")
        self.label = Label(self, image=self.img)
        self.label.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.app = app
        self.game = game
        self.gifLabel = None
        self.frames = Image.open("Images/Mowgli-Bagheera.gif").n_frames
        self.gifImages = [PhotoImage(file="Images/Mowgli-Bagheera.gif", format=f"gif -index {i}") for i in range(self.frames)]
        self.shuffleBingo()
        self.createWidgets()
        
    def createWidgets(self):
        for i in range(0, len(self.game.labels)):
            for j in range(0, len(self.game.labels)):
                button = Button(self, bg="#CCFFE5", activebackground="#CCFFE5", borderwidth=1, wraplength=100, justify=CENTER, text=self.game.labels[i][j], font=("MV Boli", 10, "bold"), relief="solid", height=8, width=20)
                button.configure(command=lambda button=button, x=i, y=j: self.buttonClick(button, x, y))
                #Pad top left
                if j == 0 and i == 0:
                    button.grid(row=i, column=j, padx=(25, 0), pady=(20, 0))
                #Pad left side of grid
                elif j == 0:
                    button.grid(row=i, column=j, padx=(25, 0))
                #Pad top side of grid
                elif i == 0:
                    button.grid(row=i, column=j, pady=(20, 0))
                else:
                    button.grid(row=i, column=j)
    
        shuffleButton = Button(self, bg="#4F5F52", fg="white", activebackground="#4F5F52", activeforeground="white", borderwidth=2, text="Shuffle", font=("Helvetica", 10, "bold"), height=4, width=20, relief="solid", command=lambda: self.shuffleBingo())
        shuffleButton.place(x=80, y=620)
        labelButton = Button(self, bg="#4F5F52", fg="white", activebackground="#4F5F52", activeforeground="white", borderwidth=2, text="Change contents", font=("Helvetica", 10, "bold"), height=4, width=20, relief="solid", command=lambda: self.app.switchFrame(SettingsFrame.__name__))
        labelButton.place(x=550, y=620)
        
    def buttonClick(self, button, x, y):
        state = self.game.state
        self.game.updateState(x, y)
        
        #Green if checked
        if state[x][y] == 1:
            button.configure(bg="#00FF80")
        else:
            button.configure(bg="#CCFFE5")
        
        #Display win text
        if self.game.checkWin():
            if self.gifLabel is None:
                self.gifLabel = Label(self, image="")
                self.gifLabel.place(x=345, y=625)
                self.animation(0, None)
        elif self.gifLabel is not None:
            self.gifLabel.destroy()
            self.gifLabel = None
    
    def shuffleBingo(self):
        self.game.randomiseLabels()
        self.game.resetState()
        self.createWidgets()
        
        if self.gifLabel is not None:
            self.gifLabel.destroy()
            self.gifLabel = None
            
    def animation(self, count, animate):
        if self.gifLabel is None:
            return
        
        image = self.gifImages[count]
        self.gifLabel.configure(image=image)
        count += 1
        if count == self.frames:
            count = 0
        #Recurse and set next image in GIF
        animate = self.after(50, lambda : self.animation(count, animate))

class SettingsFrame(Frame):
    def __init__(self, parent, app, game):
        Frame.__init__(self, parent)
        self.img = PhotoImage(file="Images/Mowgli.png")
        self.label = Label(self, image=self.img)
        self.label.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.app = app
        self.game = game
        self.texts = []
        self.createWidgets()
        
    def createWidgets(self):
        #2D list -> 1D list
        labels = np.array(self.game.labels).ravel().tolist()
        #Create text boxes in 2 columns
        for i in range(0, len(labels) // 2):
            leftText = Text(self, bg="#CCFFE5", borderwidth=2, height=4, width=40, relief="solid", padx=10, insertwidth=1)
            rightText = Text(self, bg="#CCFFE5", borderwidth=2, height=4, width=40, relief="solid", padx=10, insertwidth=1)
            leftText.insert(INSERT, labels[i])
            rightText.insert(INSERT, labels[i + len(labels) // 2])
            
            if i == 0:
                leftText.grid(row=i, column=0, padx=(60, 20), pady=(10, 1))
                rightText.grid(row=i, column=1, pady=(10, 1))
            else:
                leftText.grid(row=i, column=0, padx=(60, 20), pady=(1, 1))
                rightText.grid(row=i, column=1, pady=(1, 1))
            
            self.texts.append(leftText)
            self.texts.append(rightText)
            
        saveButton = Button(self, bg="#4F5F52", fg="white", activebackground="#4F5F52", activeforeground="white", borderwidth=2, text="Save settings", font=("Helvetica", 10, "bold"), height=4, width=25, relief="solid", command=lambda: self.saveSettings())
        saveButton.place(x=120, y=600)
        leaveButton = Button(self, bg="#4F5F52", fg="white", activebackground="#4F5F52", activeforeground="white", borderwidth=2, text="Go back", font=("Helvetica", 10, "bold"), height=4, width=25, relief="solid", command=lambda: self.resetText())
        leaveButton.place(x=500, y=600)
    
    def resetText(self):
        #2D list -> 1D list
        labels = np.array(self.game.labels).ravel().tolist()
        for i in range(0, len(labels) // 2):
            #Clear text boxes
            self.texts[i * 2].delete(1.0, END)
            self.texts[i * 2 + 1].delete(1.0, END)
            #Insert labels
            self.texts[i * 2].insert(INSERT, labels[i])
            self.texts[i * 2 + 1].insert(INSERT, labels[i + len(labels) // 2])
        
        self.app.switchFrame(MainFrame.__name__)
    
    def saveSettings(self):
        newLabels = []
        for text in self.texts:
            label = text.get(1.0, END).strip("\n")
            if label.isspace() or label == "":
                label = "FREE"
            newLabels.append(label)
        
        newLabels = np.array(newLabels).reshape(4, 4)
        self.game.changeLabels(newLabels.tolist())