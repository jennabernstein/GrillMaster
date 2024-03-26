from . import LevelManager, EventMenu, TextEntry
from engines import ThreadedGameEngine
from FSMs import LevelFSM, LevelProgressFSM
from utils import RESOLUTION
import threading
import time
from utils import vec

class LevelManagerThreaded(LevelManager):   
    def __init__(self, screenSize):      
        super().__init__(3)      
        self.loadingScreen = EventMenu("kitchen background.png", fontName="default8")
        self.loadingScreen.addOption((100,100), "Loading", RESOLUTION // 2, eventLambda = False, center="both")                               
        self.level = [ThreadedGameEngine() for x in range(3)]
        self.state = LevelFSM(self, 3)

    def draw(self, surface):      
        print(self.state.current_state_value)
        if self.state.current_state_value == "activeLevel":
            super().draw(surface)
        elif self.state.current_state_value == "loading":
            self.loadingScreen.draw(surface)
