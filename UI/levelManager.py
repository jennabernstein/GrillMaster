from FSMs import LevelFSM
from engines import GameEngine, InstructionsEngine, GameEngine2, GameEngine3, ThreadedGameEngine
import pygame

class LevelManager:
    def __init__(self, numLevels=3):
        self.levels = [ThreadedGameEngine() for _ in range(numLevels)]
        self.state = LevelFSM(self, numLevels)

    def update(self, seconds):
        if self.state.current_state.id == "activeLevel":
            self.levels[self.state.currentLevel].update(seconds)

    def handleEvent(self, event):
        if self.state.current_state.id == "activeLevel":
            self.levels[self.state.currentLevel].handleEvent(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                self.state.nextLevel()

    def draw(self, drawSurface):
        if self.state.current_state.id == "activeLevel":
            self.levels[self.state.currentLevel].draw(drawSurface)
