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


    assemble = plate.to(bun) | bun.to(patty) | patty.to(tomato) | patty.to(lettuce) | patty.to(cheese) | tomato.to(lettuce) | tomato.to(cheese) | lettuce.to(cheese) | lettuce.to(tomato) | cheese.to(lettuce) | cheese.to(tomato)

    def updateBurger(self, item):
        if item not in self.meal:
            if self.current_state.id == 'plate' and item == 'bun':
                self.assemble()
            elif self.current_state.id == 'bun' and item == 'cooked patty':
                self.assemble()
            elif self.current_state.id == 'cooked patty' and item == 'tomato':
                self.assemble()
            elif self.current_state.id == 'cooked patty' and item == 'lettuce':
                self.assemble()
            elif self.current_state.id == 'cooked patty' and item == 'cheese':
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

    def is_burger_ready(self):
        return self.current_state == self.patty or self.current_state == self.tomato or self.current_state == self.lettuce or self.current_state == self.cheese

    def reset(self):
        # Reset the FSM to its initial state
        self.current_state = self.plate
        self.meal = []

    def getStateImage(self, position):
        if self.meal == []:
            return Drawable(position, "food/plate.png", None, 0.4)
        elif self.meal == ['bun']:
            return Drawable(position, "food/burger/bun.png", None, 0.25)
        elif 'cooked patty' in self.meal and 'bun' in self.meal and len(self.meal) == 2:
            return Drawable(position, "food/burger/patty.png", None, 0.25)
        elif 'cooked patty' in self.meal and 'bun' in self.meal and 'cheese' in self.meal and len(self.meal) == 3:
            return Drawable(position, "food/burger/cheese.png", None, 0.25)
        elif 'cooked patty' in self.meal and 'bun' in self.meal and 'tomato' in self.meal and len(self.meal) == 3:
            return Drawable(position, "food/burger/tomato.png", None, 0.25)
        elif 'cooked patty' in self.meal and 'bun' in self.meal and 'lettuce' in self.meal and len(self.meal) == 3:
            return Drawable(position, "food/burger/lettuce.png", None, 0.25)
        elif 'cooked patty' in self.meal and 'bun' in self.meal and 'tomato' in self.meal and 'cheese' in self.meal and len(self.meal) == 4:
            return Drawable(position, "food/burger/cheese and tomato.png", None, 0.25)
        elif 'cooked patty' in self.meal and 'bun' in self.meal and 'tomato' in self.meal and 'lettuce' in self.meal and len(self.meal) == 4:
            return Drawable(position, "food/burger/lettuce and tomato.png", None, 0.25)
        elif 'cooked patty' in self.meal and 'bun' in self.meal and 'lettuce' in self.meal and 'cheese' in self.meal and len(self.meal) == 4:
            return Drawable(position, "food/burger/lettuce and cheese.png", None, 0.25)
        elif 'cooked patty' in self.meal and 'bun' in self.meal and 'lettuce' in self.meal and 'cheese' in self.meal and 'tomato' in self.meal and len(self.meal) == 5:
            return Drawable(position, "food/burger/cheese, tomato, lettuce.png", None, 0.25)
