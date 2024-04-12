from FSMs import ScreenManagerFSM
from . import EventMenu, LevelManagerThreaded
from engines import GameEngine, ThreadedGameEngine
from utils import vec, RESOLUTION
from gameObjects import TextEntry

from pygame.locals import *

class ScreenManager(object):
      
    def __init__(self):
        self.threadedGame = ThreadedGameEngine()  # Initialize game engine
        self.state = ScreenManagerFSM(self)
        self.current_level = self.threadedGame.levelProgress.current_state_value
        self.game = self.threadedGame.getGameEngine()
        
        self.instructions = False
        
        self.mainMenu = EventMenu("kitchen background.png", fontName="default")    
        self.mainMenu.addOption("exit", "Press esc to exit Game",
                                 RESOLUTION // 2 + vec(0,50),
                                 lambda x: x.type == KEYDOWN and x.key == K_e,
                                 center="both", color=(0,0,0))
        self.mainMenu.addOption("instructions", "Press t for a tutorial",
                                        RESOLUTION // 2,
                                        lambda x: x.type == KEYDOWN and x.key == K_t,
                                        center="both", color=(0,0,0))
        

        
        # Initializing other menus
        self.completedLevelMenu = EventMenu("kitchen background.png", fontName="default")
        self.completedLevelMenu.addText("Level Passed!", RESOLUTION // 2 - vec(175,100), 100, center="both")
        self.completedLevelMenu.addOption("return", "Press m to return to main menu", 
                                        RESOLUTION // 2, lambda x: x.type == KEYDOWN and x.key == K_m,
                                        center="both", color=(0,0,0))
        

        self.levelOverMenu = EventMenu("kitchen background.png", fontName="default")
        self.levelOverMenu.addText("Level Failed!", RESOLUTION // 2 - vec(175,100), 100, center="both")
        self.levelOverMenu.addOption("return", "Press m to return to main menu", 
                                    RESOLUTION // 2, lambda x: x.type == KEYDOWN and x.key == K_m,
                                    center="both", color=(0,0,0))
        
        self.gameStarted = False
    
    def draw(self, drawSurf):
        if self.state.isInGame():
            self.threadedGame.draw(drawSurf)

        elif self.state == "mainMenu":
            self.mainMenu.draw(drawSurf)
        if self.game.getGameOver()[0]:
            if self.state == "passedMenu":
                self.completedLevelMenu.clear()  # Clear previous score
                self.completedLevelMenu.addText("Level Passed!", RESOLUTION // 2 - vec(175,100), 100, center="both")
                self.completedLevelMenu.addOption("return", "Press m to return to main menu", 
                                                RESOLUTION // 2, lambda x: x.type == KEYDOWN and x.key == K_m,
                                                center="both", color=(0,0,0))
                self.completedLevelMenu.addText("Score: " + str(self.game.getGameOver()[1]) + "/" + str(self.game.getGameOver()[2]), RESOLUTION // 2 - vec(200,50), 100, center="both")
                self.completedLevelMenu.draw(drawSurf)
            elif self.state == "failedMenu":
                self.levelOverMenu.clear()  # Clear previous score
                self.levelOverMenu.addText("Level Failed!", RESOLUTION // 2 - vec(175,100), 100, center="both")
                self.levelOverMenu.addOption("return", "Press m to return to main menu", 
                                            RESOLUTION // 2, lambda x: x.type == KEYDOWN and x.key == K_m,
                                            center="both", color=(0,0,0))
                self.levelOverMenu.addText("Score: " + str(self.game.getGameOver()[1]) + "/" + str(self.game.getGameOver()[2]), RESOLUTION // 2 - vec(200,50), 100, center="both")
                self.levelOverMenu.draw(drawSurf)



    def handleEvent(self, event):
        if self.state in ["instructions", "level1", "level2"]:
            if event.type == KEYDOWN and event.key == K_m:
                self.state.quitGame()
            else:
                self.threadedGame.handleEvent(event)
        elif self.state == "mainMenu":
            choice = self.mainMenu.handleEvent(event)            
            if choice == "instructions":
                self.instructions = True
                self.threadedGame.setCurrentGame('instructions')
                self.game = self.threadedGame.getGameEngine(self.instructions)
                self.state.startInstructions()
            elif choice == "level_1":
                self.state.startLevel1()
            elif choice == "level_2":
                self.state.startLevel2()
            elif choice == "exit":
                return "exit"
        elif self.state == "passedMenu":
            choice = self.completedLevelMenu.handleEvent(event)
            if choice == "return":
                self.threadedGame.setNewGame(self.threadedGame.levelProgress.current_state_value)
                self.state.toMain()
        elif self.state == "failedMenu":
            choice = self.levelOverMenu.handleEvent(event)
            if choice == "return":
                self.threadedGame.setNewGame(self.threadedGame.levelProgress.current_state_value)
                self.state.toMain()

    
    def update(self, seconds):  
        self.game = self.threadedGame.getGameEngine(self.instructions)
        if self.game.getGameOver()[0]:
            if self.game.passed() and self.state != "mainMenu":  # Check if not already in passedMenu state
                self.threadedGame.levelProgress.completeLevel(self.current_level)
                self.current_level = self.threadedGame.levelProgress.current_state_value
                self.state.passed()  # Transition to passedMenu state
            elif not self.game.passed() and self.state != "mainMenu":  # Check if not already in failedMenu state
                self.threadedGame.levelProgress.failedLevel()
                self.state.failed()  # Transition to failedMenu state
            if self.state == "passedMenu":
                self.completedLevelMenu.update(seconds)
            elif self.state == "failedMenu":
                self.levelOverMenu.update(seconds)
                
        if self.state in ["level1", "level2"]:
            self.threadedGame.update(seconds)
        elif self.instructions:
            self.game.update(seconds)
        elif self.state == "mainMenu":
            if self.threadedGame.levelProgress.current_state_value == 'level1':
                self.mainMenu.addOption("level_1", "Press 1 to start Level 1",
                                        RESOLUTION // 2 - vec(0,100),
                                        lambda x: x.type == KEYDOWN and x.key == K_1,
                                        center="both", color=(0,0,0))
            if self.threadedGame.levelProgress.current_state_value == 'level2':
                self.mainMenu.addOption("level_2", "Press 2 to start Level 2",
                                        RESOLUTION // 2 - vec(0,50),
                                        lambda x: x.type == KEYDOWN and x.key == K_2,
                                        center="both", color=(0,0,0))
            self.mainMenu.update(seconds)
