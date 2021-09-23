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
        self.checkedLabels  = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        
    def checkWin(self):
        for row in self.checkedLabels:
            if row[0] == 1 and row.count(row[0]) == len(row):
                return True
        
        transposedLabels = np.transpose(self.labels)
        for row in transposedLabels:
            if row[0] == 1 and row.count(row[0]) == len(row):
                return True
            
        for i in range (0, len(self.checkedLabels) - 1):
            if self.labels[i][i] == 0:
                break
        
        for i in range (0, len(self.checkedLabels) - 1):
            if self.labels[i][len(self.checkedLabels) - 1 - i] == 0:
                break
            
        return False
    
    def updateLabelState(self, x, y):
        if self.checkedLabels[x][y] == 0:
            self.checkedLabels[x][y] = 1
        else:
            self.checkedLabels[x][y] = 0

def randomiseLabels():
    labels = np.array(LABELS)
    random.shuffle(labels)
    
    return labels.reshape(4, 4)
    