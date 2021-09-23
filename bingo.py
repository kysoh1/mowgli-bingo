import numpy as np
import random

LABELS = ["FREE", 
          "'I played that so well'", 
          "Unintelligible moaning", 
          "Has incorrect runes", 
          "Initiates an FF vote", 
          "Types in all chat asking if there are any single ladies", 
          "Picks an assassin champion",
          "Praises himself after making a play",
          "Switches to ARAM after losing a normal game",
          "Picks Nasus",
          "Picks Evelynn",
          "Leaves voice chat without saying goodbye",
          "Goes to eat dinner then comes back immediately and asks you to stream the game",
          "'I think we lost this one' (Must be said in champ select)",
          "Gets camped by jungler during laning phase",
          "Gets solo killed within the first 15 minutes"]

class Game():
    def __init__(self, labels):
        self.labels = labels
        self.state  = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        
    def checkWin(self):
        #Check rows
        for row in self.state:
            if row[0] == 1 and row.count(row[0]) == len(row):
                return True
        
        #Check columns
        state = np.array(self.state)
        transposedState = np.transpose(state)
        for row in transposedState:
            #Convert numpy array to list
            row = row.tolist()
            if row[0] == 1 and row.count(row[0]) == len(row):
                return True
        
        #Check diagonals
        diagOne = True
        diagTwo = True
        for i in range (0, len(self.state)):
            #Initial check, false if both diagonals have a 0
            if self.state[i][i] == 0 and self.state[i][len(self.state) - 1 - i] == 0:
                diagOne = False
                diagTwo = False
                break
            
            #Top left to bottom right
            if self.state[i][i] == 0:
                diagOne = False
            
            #Bottom left to top right
            if self.state[i][len(self.state) - 1 - i] == 0:
                diagTwo = False
            
        if diagOne or diagTwo:
            return True

        return False
    
    def updateState(self, x, y):
        if self.state[x][y] == 0:
            self.state[x][y] = 1
        else:
            self.state[x][y] = 0

def randomiseLabels():
    labels = np.array(LABELS)
    random.shuffle(labels)
    
    return labels.reshape(4, 4)
    