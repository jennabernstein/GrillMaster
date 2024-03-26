from statemachine import State
from .abstract import AbstractGameFSM
from gameObjects import Drawable

class HotDogMealFSM(AbstractGameFSM):
    def __init__(self, obj):
        super().__init__(obj)
        self.meal = []

    plate = State('plate', initial=True)
    bun = State('bun')
    hotdog = State('hot dog')
    

    drop_off_without_assembly = plate.to(hotdog) | hotdog.to(plate)
    assemble = plate.to(bun) | bun.to(hotdog) | hotdog.to(hotdog)

    def updateHotDog(self, item):
        print(item)
        if item not in self.meal:
            if self.current_state.id == 'plate' and item == 'hot dog bun':
                self.assemble()
            elif self.current_state.id == 'bun' and item == 'cooked hot dog meat':
                self.assemble()
            print(self.current_state.id)
            self.meal.append(item)
        if item.split()[0] == 'hot dog meal':
            self.drop_off_without_assembly()

    def is_hotdog_ready(self):
        return self.current_state == self.hotdog

    def set_current_state(self, state, meal):
        self.current_state = state
        self.meal = meal

    def reset(self):
        # Reset the FSM to its initial state
        self.current_state = self.plate
        self.meal = []

    def getMeal(self):
        return self.meal

    def getStateImage(self, position):
        print(self.meal)
        if self.meal == []:
            meal = Drawable(position, "food/plate.png", None, 0.4)
        elif self.meal == ['hot dog bun']:
            meal =  Drawable(position, "food/hot dog/hot dog bun with plate.png", None, 0.3)
        elif 'hot dog bun' in self.meal and 'cooked hot dog meat' in self.meal and len(self.meal) == 2:
            meal = Drawable(position, "food/hot dog/cooked hot dog with plate.png", None, 0.3)
            meal.stateType = 'hot dog meal'
        return meal