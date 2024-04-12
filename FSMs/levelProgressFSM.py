from FSMs import AbstractGameFSM
from statemachine import State

class LevelProgressFSM(AbstractGameFSM):
    level1 = State(initial=True)
    level2 = State()

    failedLevel = level1.to(level1) | level2.to(level2)
    completeLevel1 = level1.to(level2)
    completeLevel2 = level2.to(level2)

    def getLevelState(self):
        return self.current_state

    
    def completeLevel(self, current_level):

        if current_level == 'level1':
            self.completeLevel1()
        elif current_level == 'level2':
            self.completeLevel2()
    
    def getLevelGameEngine(self):

        if self.current_state == self.level1:
            return 'GameEngine2'
        elif self.current_state == self.level2:
            return 'GameEngine3'