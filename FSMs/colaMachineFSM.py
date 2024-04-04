from . import AbstractGameFSM
from statemachine import State
from gameObjects import Drawable

class ColaMachineFSM(AbstractGameFSM):
    empty = State('empty', initial=True)
    one_can = State('one can')
    two_cans = State('two cans')
    three_cans = State('three cans')

    add_can = empty.to(one_can) | one_can.to(two_cans) | two_cans.to(three_cans) | three_cans.to(three_cans)
    take_can = three_cans.to(two_cans) | two_cans.to(one_can) | one_can.to(empty) | empty.to(empty)


    def update_machine(self):
        self.add_can()
    
    def takeCan(self):
        self.take_can()
    
    def is_ready(self):
        return self.current_state in [self.one_can, self.two_cans, self.three_cans]

    def update_image(self):
        return self.machine_image
    
    def reset(self):
        # Reset the FSM to its initial state
        self.current_state = self.empty

    def getStateImage(self, position):
        if self.current_state == self.empty:
            self.machine_image = Drawable(position, "cola machine.png", (0,0), scale=0.8)
        if self.current_state == self.one_can:
            self.machine_image = Drawable(position, "cola machine.png", (1,0), scale=0.8)
        elif self.current_state == self.two_cans:
            self.machine_image = Drawable(position, "cola machine.png", (2,0), scale=0.8)
        elif self.current_state == self.three_cans:
            self.machine_image = Drawable(position, "cola machine.png", (3,0), scale=0.8)
        return self.machine_image
    