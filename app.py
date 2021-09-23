from tkinter import *
from PIL import ImageTk
from PIL import Image
import bingo
import numpy as np

class Application(Frame):
    def __init__(self, root=None):
        super().__init__(root)
        self.root = root
        self.game = bingo.Game(bingo.randomiseLabels())
        self.buttons = None
        self.create_widgets()

    def create_widgets(self):
        rowIdx = 0
        columnIdx = 0
        labels = self.game.labels
        for row in labels:
            for label in row:
                button = Button(self.root, wraplength=80, justify=CENTER, bg="white", text=label, height=8, width=21, command=lambda x=rowIdx, y=columnIdx: self.buttonClick(x, y))
                #Pad top left
                if columnIdx == 0 and rowIdx == 0:
                    button.grid(row=rowIdx, column=columnIdx, padx=(80, 0), pady=(80, 0))
                #Pad left side of grid
                elif columnIdx == 0:
                    button.grid(row=rowIdx, column=columnIdx, padx=(80, 0))
                #Pad top side of grid
                elif rowIdx == 0:
                    button.grid(row=rowIdx, column=columnIdx, pady=(80, 0))
                else:
                    button.grid(row=rowIdx, column=columnIdx)
                
                columnIdx = columnIdx + 1
                
            rowIdx = rowIdx + 1
            columnIdx = 0
        
    def buttonClick(self, x, y):
        print(x, y)

root = Tk()
root.iconbitmap("Mowgli.ico")
root.geometry("800x700")

bg = PhotoImage(file="Mowgli.png")
bgLabel = Label(root, image=bg)
bgLabel.place(x=0, y=0, relwidth=1, relheight=1)

app = Application(root=root)
app.master.title("Bingo!")
app.master.minsize(800, 700)
app.master.maxsize(800, 700)

app.mainloop()