from . import AbstractGameFSM
from statemachine import State
from gameObjects import Drawable

class PattyFSM(AbstractGameFSM):
    raw = State('raw', initial=True)
    cooking = State('cooking')
    cooked = State('cooked')
    burnt = State('burnt')

    cook = raw.to(cooking) | cooking.to(cooked) | cooked.to(burnt) | burnt.to(burnt)

    def update_cooking(self, seconds):
        self.seconds = seconds
        if self.current_state == self.burnt:
            self.cook()
        elif seconds >= 15 and self.current_state == self.cooked:
            self.cook()
        elif seconds >= 10 and self.current_state == self.cooking:
            self.cook()
        elif seconds >= 5 and self.current_state == self.raw:
            self.cook()

    def is_done_cooking(self):
        return self.current_state == self.cooked or self.current_state == self.burnt
    
    def is_ready(self):
        return self.current_state == self.cooked

    def is_burnt(self):
        return self.current_state == self.burnt

    def update_image(self):
        return self.patty_image
    
    def reset(self):
        # Reset the FSM to its initial state
        self.current_state = self.raw

    def getStateImage(self, position, offset):
        if self.current_state == self.raw:
            self.patty_image = Drawable(position, "food/burger sprites.png", (offset, 0), 0.5)
            self.patty_image.stateType = 'raw patty'
        elif self.current_state == self.cooking:
            self.patty_image = Drawable(position, "food/burger sprites.png", (offset, 1), 0.5)
            self.patty_image.stateType = 'cooking patty'
        elif self.current_state == self.cooked:
            self.patty_image = Drawable(position, "food/burger sprites.png", (offset, 2), 0.5)
            self.patty_image.stateType = 'cooked patty'
        elif self.current_state == self.burnt:
            self.patty_image = Drawable(position, "food/burger sprites.png", (offset, 3), 0.5)
            self.patty_image.stateType = 'burnt patty'
        return self.patty_image
    
    def get_cooking_percentage(self):
        return self.seconds/10