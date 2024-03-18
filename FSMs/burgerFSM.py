from statemachine import State
from .abstract import AbstractGameFSM
from gameObjects import Drawable

class BurgerFSM(AbstractGameFSM):
    def __init__(self, obj):
        super().__init__(obj)
        self.meal = []

    plate = State('plate', initial=True)
    bun = State('bun')
    patty = State('cooked patty')
    tomato = State('tomato')
    lettuce = State('lettuce')
    cheese = State('cheese')
    burger = State('burger')

    drop_off_without_assembly = plate.to(burger) | burger.to(plate)
    assemble = plate.to(bun) | bun.to(patty) | patty.to(tomato) | patty.to(lettuce) | patty.to(cheese) | tomato.to(lettuce) | tomato.to(cheese) | lettuce.to(cheese) | lettuce.to(tomato) | cheese.to(lettuce) | cheese.to(tomato)

    def updateBurger(self, item):
        if item not in self.meal:
            if self.current_state.id == 'plate' and item == 'bun':
                self.assemble()
            elif self.current_state.id == 'bun' and (item == 'cooked meat patty' or item == 'cooked vegan patty'):
                self.assemble()
            elif (self.current_state.id == 'cooked vegan patty' or self.current_state.id == 'cooked meat patty') and item == 'tomato':
                self.assemble()
            elif (self.current_state.id == 'cooked vegan patty' or self.current_state.id == 'cooked meat patty') and item == 'lettuce':
                self.assemble()
            elif (self.current_state.id == 'cooked vegan patty' or self.current_state.id == 'cooked meat patty') and item == 'cheese':
                self.assemble()
            elif self.current_state.id == 'tomato' and item == 'lettuce':
                self.assemble()
            elif self.current_state.id == 'tomato' and item == 'cheese' :
                self.assemble()
            elif self.current_state.id == 'lettuce' and item == 'cheese':
                self.assemble()
            elif self.current_state.id == 'lettuce' and item == 'tomato':
                self.assemble()
            elif self.current_state.id == 'cheese' and item == 'lettuce':
                self.assemble()
            elif self.current_state.id == 'cheese' and item == 'tomato':
                self.assemble()
            self.meal.append(item)
        if item.split()[0] == 'burger':
            self.drop_off_without_assembly()

    def is_burger_ready(self):
        return self.current_state == self.patty or self.current_state == self.tomato or self.current_state == self.lettuce or self.current_state == self.cheese

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
        if self.meal == []:
            meal = Drawable(position, "food/plate.png", None, 0.4)
        elif self.meal == ['bun']:
            meal =  Drawable(position, "food/burger/bun with plate.png", None, 0.3)
        elif ('cooked vegan patty' in self.meal or 'cooked meat patty' in self.meal) and 'bun' in self.meal and len(self.meal) == 2:
            meal = Drawable(position, "food/burger/patty with plate.png", None, 0.3)
            meal.stateType = 'burger with '
            if 'cooked vegan patty' in self.meal:
                meal.stateType += 'cooked vegan patty'
            elif 'cooked meat patty' in self.meal:
                meal.stateType += 'cooked meat patty'
        elif ('cooked vegan patty' in self.meal or 'cooked meat patty' in self.meal) and 'bun' in self.meal and 'cheese' in self.meal and len(self.meal) == 3:
            meal = Drawable(position, "food/burger/cheese with plate.png", None, 0.3)
            meal.stateType = 'burger with '
            if 'cooked vegan patty' in self.meal:
                meal.stateType += 'cooked vegan patty'
            elif 'cooked meat patty' in self.meal:
                meal.stateType += 'cooked meat patty'
            meal.stateType += ', cheese'
        elif ('cooked vegan patty' in self.meal or 'cooked meat patty' in self.meal) and 'bun' in self.meal and 'tomato' in self.meal and len(self.meal) == 3:
            meal = Drawable(position, "food/burger/tomato with plate.png", None, 0.3)
            meal.stateType = 'burger with '
            if 'cooked vegan patty' in self.meal:
                meal.stateType += 'cooked vegan patty'
            elif 'cooked meat patty' in self.meal:
                meal.stateType += 'cooked meat patty'
            meal.stateType += ', tomato'
        elif ('cooked vegan patty' in self.meal or 'cooked meat patty' in self.meal) and 'bun' in self.meal and 'lettuce' in self.meal and len(self.meal) == 3:
            meal = Drawable(position, "food/burger/lettuce with plate.png", None, 0.3)
            meal.stateType = 'burger with '
            if 'cooked vegan patty' in self.meal:
                meal.stateType += 'cooked vegan patty'
            elif 'cooked meat patty' in self.meal:
                meal.stateType += 'cooked meat patty'
            meal.stateType += ', lettuce'
        elif ('cooked vegan patty' in self.meal or 'cooked meat patty' in self.meal) and 'bun' in self.meal and 'tomato' in self.meal and 'cheese' in self.meal and len(self.meal) == 4:
            meal = Drawable(position, "food/burger/cheese and tomato with plate.png", None, 0.3)
            meal.stateType = 'burger with '
            if 'cooked vegan patty' in self.meal:
                meal.stateType += 'cooked vegan patty'
            elif 'cooked meat patty' in self.meal:
                meal.stateType += 'cooked meat patty'
            meal.stateType += ', tomato, cheese'
        elif ('cooked vegan patty' in self.meal or 'cooked meat patty' in self.meal) and 'bun' in self.meal and 'tomato' in self.meal and 'lettuce' in self.meal and len(self.meal) == 4:
            meal = Drawable(position, "food/burger/lettuce and tomato with plate.png", None, 0.3)
            meal.stateType = 'burger with '
            if 'cooked vegan patty' in self.meal:
                meal.stateType += 'cooked vegan patty'
            elif 'cooked meat patty' in self.meal:
                meal.stateType += 'cooked meat patty'
            meal.stateType += ', tomato, lettuce'
        elif ('cooked vegan patty' in self.meal or 'cooked meat patty' in self.meal) and 'bun' in self.meal and 'lettuce' in self.meal and 'cheese' in self.meal and len(self.meal) == 4:
            meal =  Drawable(position, "food/burger/lettuce and cheese with plate.png", None, 0.3)
            meal.stateType = 'burger with '
            if 'cooked vegan patty' in self.meal:
                meal.stateType += 'cooked vegan patty'
            elif 'cooked meat patty' in self.meal:
                meal.stateType += 'cooked meat patty'
            meal.stateType += ', cheese, lettuce'
        elif ('cooked vegan patty' in self.meal or 'cooked meat patty' in self.meal) and 'bun' in self.meal and 'lettuce' in self.meal and 'cheese' in self.meal and 'tomato' in self.meal and len(self.meal) == 5:
            meal = Drawable(position, "food/burger/cheese, tomato, lettuce with plate.png", None, 0.3)
            meal.stateType = 'burger with '
            if 'cooked vegan patty' in self.meal:
                meal.stateType += 'cooked vegan patty'
            elif 'cooked meat patty' in self.meal:
                meal.stateType += 'cooked meat patty'
            meal.stateType += ', cheese, tomato, lettuce'
        return meal