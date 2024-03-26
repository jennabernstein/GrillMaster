from statemachine import State
from .abstract import AbstractGameFSM
from gameObjects import Drawable

class MealFSM(AbstractGameFSM):
    def __init__(self, obj):
        super().__init__(obj)
        self.meal = []
        self.position = (0,0)

    plate = State('plate', initial=True)
    burger = State('meal')

    assemble = plate.to(burger) | burger.to(plate)

    def updateMeal(self, item):
        if self.current_state.id == 'plate' and (item.getStateType().split()[0] == 'burger' or item.getStateType() == 'hot dog meal'):
            self.assemble()
        elif self.current_state.id == 'meal' and item.getStateType() == 'ticket':
            self.assemble()

    def setBurger(self, burger):
        self.burger = burger

    def setHotDog(self, hotdog):
        self.hotdog = hotdog

    def reset(self):
        self.current_state = self.plate
        self.meal = []

    def getMeal(self):
        return self.meal

    def getStateImage(self, item, position):
        if item is not None:
            if 'hot dog meal' == item.getStateType() and 'hot dog meal' not in self.meal:
                self.meal.append('hot dog meal')
            if self.current_state.id == 'hot dog meal' and item.getStateType() == 'ticket':
                    self.reset()
            else:
                if 'bun' not in self.meal:
                    self.meal.append('bun')
                if 'cooked vegan patty' in item.getStateType() and 'cooked vegan patty' not in self.meal:
                    self.meal.append('cooked vegan patty')
                if 'cooked meat patty' in item.getStateType() and 'cooked meat patty' not in self.meal:
                    self.meal.append('cooked meat patty')
                if 'cheese' in item.getStateType() and 'cheese' not in self.meal:
                    self.meal.append('cheese')
                if 'tomato' in item.getStateType() and 'tomato' not in self.meal:
                    self.meal.append('tomato')
                if 'lettuce' in item.getStateType() and 'lettuce' not in self.meal:
                    self.meal.append('lettuce')
                if self.current_state.id == 'burger' and item.getStateType() == 'ticket':
                    self.reset()
            print(self.meal)

            if self.current_state.id == 'plate':
                if 'hot dog meal' == item.getStateType():
                    return Drawable(position, "food/hot dog/cooked hot dog with plate.png", None, 0.3)
                else:
                    if 'burger with cooked vegan patty' == item.getStateType() or 'burger with cooked meat patty' == item.getStateType():
                        return Drawable(position, "food/burger/patty with plate.png", None, 0.3)
                    
                    elif 'burger with cooked vegan patty, cheese' == item.getStateType() or 'burger with cooked meat patty, cheese' == item.getStateType():
                        return Drawable(position, "food/burger/cheese with plate.png", None, 0.3)
                    
                    elif 'burger with cooked vegan patty, tomato' == item.getStateType() or 'burger with cooked meat patty, tomato' == item.getStateType():
                        return Drawable(position, "food/burger/tomato with plate.png", None, 0.3)
                    
                    elif 'burger with cooked vegan patty, lettuce' == item.getStateType() or 'burger with cooked meat patty, lettuce' == item.getStateType():
                        return Drawable(position, "food/burger/lettuce with plate.png", None, 0.3)
                    
                    elif 'burger with cooked vegan patty, tomato, cheese' == item.getStateType() or 'burger with cooked meat patty, tomato, cheese' == item.getStateType():
                        return Drawable(position, "food/burger/cheese and tomato with plate.png", None, 0.3)
                    
                    elif 'burger with cooked vegan patty, tomato, lettuce' == item.getStateType() or 'burger with cooked meat patty, tomato, lettuce' == item.getStateType():
                        return Drawable(position, "food/burger/lettuce and tomato with plate.png", None, 0.3)
                    
                    elif 'burger with cooked vegan patty, cheese, lettuce' == item.getStateType() or 'burger with cooked meat patty, cheese, lettuce' == item.getStateType():
                        return Drawable(position, "food/burger/lettuce and cheese with plate.png", None, 0.3)
                    
                    elif 'burger with cooked vegan patty, cheese, tomato, lettuce' == item.getStateType() or 'burger with cooked meat patty, cheese, tomato, lettuce' == item.getStateType():
                        return Drawable(position, "food/burger/cheese, tomato, lettuce with plate.png", None, 0.3)
            return Drawable()

            