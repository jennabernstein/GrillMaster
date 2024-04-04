from . import AbstractGameFSM
from statemachine import State

class ScreenManagerFSM(AbstractGameFSM):
    mainMenu = State(initial=True)
    instructions = State()
    level1 = State()
    level2 = State()
    passedMenu = State()
    failedMenu = State()
    
    #startGame = mainMenu.to(game)
    startLevel1 = mainMenu.to(level1) | failedMenu.to(level1) | passedMenu.to(level1)
    startLevel2 = mainMenu.to(level2) | failedMenu.to(level2) | passedMenu.to(level2)
    startInstructions = mainMenu.to(instructions) | failedMenu.to(instructions) | passedMenu.to(instructions)
    passed = level1.to(passedMenu) | level2.to(passedMenu) | instructions.to(passedMenu) | passedMenu.to(passedMenu)
    failed = level1.to(failedMenu) | level2.to(failedMenu) | instructions.to(failedMenu) | failedMenu.to(failedMenu)
    quitGame  = level1.to(mainMenu) | level2.to(mainMenu) | instructions.to(mainMenu) 
    toMain = passedMenu.to(mainMenu) | failedMenu.to(mainMenu)

    def isInGame(self):
        return self == "level1" or self == "level2" or self == "instructions"