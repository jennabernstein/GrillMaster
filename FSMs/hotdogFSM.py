from . import AbstractGameFSM
from statemachine import State
from gameObjects import Drawable

class HotDogFSM(AbstractGameFSM):
    raw = State('raw', initial=True)
    cooked = State('cooked')
    burnt = State('burnt')

    cook = raw.to(cooked) | cooked.to(burnt) | burnt.to(burnt)

    def update_cooking(self, seconds):
        self.seconds = seconds
        if self.current_state == self.burnt:
            self.cook()
        elif seconds >= 15 and self.current_state == self.cooked:
            self.cook()
        elif seconds >= 10 and self.current_state == self.raw:
            self.cook()

    def is_done_cooking(self):
        return self.current_state == self.cooked or self.current_state == self.burnt
    
    def is_ready(self):
        return self.current_state == self.cooked

    def is_burnt(self):
        return self.current_state == self.burnt

    def update_image(self):
        return self.hotdog_image
    
    def reset(self):
        # Reset the FSM to its initial state
        self.current_state = self.raw

    def getStateImage(self, position):
        if self.current_state == self.raw:
            self.hotdog_image = Drawable(position, "food/hot dog/hot dog meat.png", offset=None,scale=0.3)
            self.hotdog_image.stateType = 'raw hot dog meat'
        elif self.current_state == self.cooked:
            self.hotdog_image = Drawable(position, "food/hot dog/cooked hot dog meat.png", offset=None,scale=0.17)
            self.hotdog_image.stateType = 'cooked hot dog meat'
        elif self.current_state == self.burnt:
            self.hotdog_image = Drawable(position, "food/hot dog/burnt hot dog meat.png", offset=None,scale=0.3)
            self.hotdog_image.stateType = 'burnt hot dog meat'
        return self.hotdog_image
    
    def get_cooking_percentage(self):
        return self.seconds/10