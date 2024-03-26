from . import AbstractGameFSM
from statemachine import State

class ScreenManagerFSM(AbstractGameFSM):
    mainMenu = State(initial=True)
    level1 = State()
    level2 = State()
    level3 = State()
    paused   = State()
    passedMenu = State()
    failedMenu = State()
    
    pause = level1.to(paused) | paused.to(level1) | level2.to(paused) | paused.to(level2) | level3.to(paused) | paused.to(level3) | mainMenu.to.itself(internal=True)
    #startGame = mainMenu.to(game)
    startLevel1 = mainMenu.to(level1) | failedMenu.to(level1) | passedMenu.to(level1)
    startLevel2 = mainMenu.to(level2) | failedMenu.to(level2) | passedMenu.to(level2)
    startLevel3 = mainMenu.to(level3) | failedMenu.to(level3) | passedMenu.to(level3)
    passed = level1.to(passedMenu) | level2.to(passedMenu) | level3.to(passedMenu) | passedMenu.to(passedMenu)
    failed = level1.to(failedMenu) | level2.to(failedMenu) | level3.to(failedMenu) | failedMenu.to(failedMenu)
    quitGame  = level1.to(mainMenu) | level2.to(mainMenu) | level3.to(mainMenu) | paused.to.itself(internal=True)
    toMain = passedMenu.to(mainMenu) | failedMenu.to(mainMenu)

    def isInGame(self):
        return self == "level1" or self == "level2" or self == "level3" or self == "paused"