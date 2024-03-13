from statemachine import State
from .abstract import AbstractGameFSM
from gameObjects import Drawable

class MealFSM(AbstractGameFSM):
    def __init__(self, obj):
        super().__init__(obj)

    plate = State('plate', initial=True)
    burger = State('burger')
    serve = State('serve')

    assemble = plate.to(burger) | burger.to(serve) | serve.to(plate) 

    def setBurger(self, burger):
        self.burger = burger

    def updateMeal(self, item):
        if self.current_state.id == 'plate' and item.getStateType().split()[0] == 'burger':
            self.assemble()
        elif self.current_state.id == 'burger' and item == 'serve':
            self.assemble()
    
    def reset(self):
        self.current_state = self.plate

    def getStateImage(self, item, position):
        meal = Drawable()
        if self.current_state.id == 'plate':
            if 'burger with cooked vegan patty' == item.getStateType() or 'burger with cooked meat patty' == item.getStateType():
                meal = Drawable(position, "food/burger/patty with plate.png", None, 0.3)
            
            elif 'burger with cooked vegan patty, cheese' == item.getStateType() or 'burger with cooked meat patty, cheese' == item.getStateType():
                meal = Drawable(position, "food/burger/cheese with plate.png", None, 0.3)
            
            elif 'burger with cooked vegan patty, tomato' == item.getStateType() or 'burger with cooked meat patty, tomato' == item.getStateType():
                meal = Drawable(position, "food/burger/tomato with plate.png", None, 0.3)
            
            elif 'burger with cooked vegan patty, lettuce' == item.getStateType() or 'burger with cooked meat patty, lettuce' == item.getStateType():
                meal = Drawable(position, "food/burger/lettuce with plate.png", None, 0.3)
            
            elif 'burger with cooked vegan patty, tomato, cheese' == item.getStateType() or 'burger with cooked meat patty, tomato, cheese' == item.getStateType():
                meal = Drawable(position, "food/burger/cheese and tomato with plate.png", None, 0.3)
            
            elif 'burger with cooked vegan patty, tomato, lettuce' == item.getStateType() or 'burger with cooked meat patty, tomato, lettuce' == item.getStateType():
                meal = Drawable(position, "food/burger/lettuce and tomato with plate.png", None, 0.3)
            
            elif 'burger with cooked vegan patty, cheese, lettuce' == item.getStateType() or 'burger with cooked meat patty, cheese, lettuce' == item.getStateType():
                meal =  Drawable(position, "food/burger/lettuce and cheese with plate.png", None, 0.3)
            
            elif 'burger with cooked vegan patty, cheese, tomato, lettuce' == item.getStateType() or 'burger with cooked meat patty, cheese, tomato, lettuce' == item.getStateType():
                meal = Drawable(position, "food/burger/cheese, tomato, lettuce with plate.png", None, 0.3)
        return meal

            