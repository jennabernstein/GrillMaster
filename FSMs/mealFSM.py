from statemachine import State
from .abstract import AbstractGameFSM
from gameObjects import Drawable

class MealFSM(AbstractGameFSM):
    def __init__(self, obj):
        super().__init__(obj)
        self.meal = []
        self.position = (0,0)

    plate = State('plate', initial=True)
    burger = State('burger')

    assemble = plate.to(burger) | burger.to(plate)

    def updateMeal(self, item):
        if self.current_state.id == 'plate' and item.getStateType().split()[0] == 'burger':
            self.assemble()
        elif self.current_state.id == 'burger' and item.getStateType() == 'ticket':
            self.assemble()

    def setBurger(self, burger):
        self.burger = burger

    def reset(self):
        self.current_state = self.plate
        self.meal = []

    def getMeal(self):
        return self.meal

    def getStateImage(self, item, position):
        if item is not None:
            
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
                else:
                    return Drawable()

            