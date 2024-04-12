from . import InstructionsEngine, GameEngine2, GameEngine3
import threading
import time
from FSMs import LevelProgressFSM


class ThreadedGameEngine():
    def __init__(self): 
        self.levelProgress = LevelProgressFSM(self)
        self.games = [InstructionsEngine(), GameEngine2(), GameEngine3()]
        self.game = None
    
    def getGameEngine(self, instructions=False):
        if self.levelProgress.current_state_value == 'level1':
            game = self.games[1]
        elif self.levelProgress.current_state_value == 'level2':
            game = self.games[2]
        if instructions:
            game = self.games[0]
        return game

    def setCurrentGame(self, engine):
        if engine == 'instructions':
            self.game = self.games[0]
        elif engine == 'level1':
            self.game = self.games[1]
        elif engine == 'level2':
            self.game = self.games[2]

    def setNewGame(self, level):
        if level == 'level1':
            self.games[1] = GameEngine2()
            self.game = self.games[1]
        elif level == 'level2':
            self.games[2] = GameEngine3()
            self.game = self.games[2]

    def update(self, seconds):
        if self.levelProgress.current_state_value == 'level1':
            self.game = self.games[1]
        elif self.levelProgress.current_state_value == 'level2':
            self.game = self.games[2]
        self.game.update(seconds)

    def handleEvent(self, event):
        if self.game is not None:
            self.game.handleEvent(event)

    def draw(self, surface):  
        if self.game is not None:  
            self.game.draw(surface)

    def levelOver(self):
        #if all the customers have left
        pass

    def gameOver(self):
        return self.game.getGameOver()
    
    def unpassGame(self):
        self.game.reset()

    def isComplete(self):
        return self.game.passed()
