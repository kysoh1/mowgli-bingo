import numpy as np
import random

class Game():
    def __init__(self):
        self.labels = [["FREE", 
                       "'I played that so well'", 
                       "Unintelligible moaning", 
                       "Has incorrect runes"], 
                       ["Initiates an FF vote", 
                       "Types in all chat asking if there are any single ladies", 
                       "Picks an assassin champion",
                       "Praises himself after making a play"],
                       ["Switches to ARAM after losing a normal game",
                       "Picks Nasus",
                       "Picks Evelynn",
                       "Leaves voice chat without saying goodbye"],
                       ["Goes to eat dinner then comes back immediately and asks you to stream the game",
                       "'I think we lost this one' (Must be said in champ select)",
                       "Gets camped by jungler during laning phase",
                       "Gets solo killed within the first 15 minutes"]]
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
            
        #At least one diagonal is a win
        if diagOne or diagTwo:
            return True

        return False
    
    def updateState(self, x, y):
        if self.state[x][y] == 0:
            self.state[x][y] = 1
        else:
            self.state[x][y] = 0
    
    def resetState(self):
        for i in range(0, len(self.state)):
            for j in range(0, len(self.state)):
                self.state[i][j] = 0
    
    def randomiseLabels(self):
        npLabels = np.array(self.labels)
        npLabels = npLabels.ravel()
        random.shuffle(npLabels)
        npLabels = npLabels.reshape(4, 4)
        self.labels = npLabels.tolist()
        
    def changeLabels(self, newLabels):
        self.labels = newLabels
        