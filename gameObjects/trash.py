from .drawable import Drawable

class Trash(Drawable):
    def __init__(self, position, offset):
        super().__init__(position, "trash cans.png", offset)
        self.nFrames = 2
        self.opened = False
        self.chefPos = (300,300)

    def open_can(self):
        self.opened = True

    def close_can(self):
        self.opened = False

    def is_open(self):
        return self.opened
    
    def update(self, seconds):
        super().update(seconds)

