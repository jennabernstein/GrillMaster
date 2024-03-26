from FSMs import AbstractGameFSM
from statemachine import State
        
class LevelFSM(AbstractGameFSM):
    loading = State(initial=True)
    activeLevel = State()
    
    nextLevel = loading.to(activeLevel) | activeLevel.to(activeLevel) # Transition from loading to activeLevel
    
    def __init__(self, obj, maxLevels):
        self.currentLevel = -1
        self.maxLevels = maxLevels
        super().__init__(obj)
            
    def isLoaded(self):
        return self.obj.levels[self.currentLevel].loaded   
    
    def on_enter_loading(self):
        if self.currentLevel < self.maxLevels - 1:
            self.currentLevel += 1
        print(self.currentLevel)
