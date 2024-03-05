from .drawable import Drawable

class Trash(Drawable):
    def __init__(self, position, offset):
        super().__init__(position, "trash cans.png", offset)
        self.offset = offset
        self.nFrames = 2
        self.opened = False
        self.chefPos = (-20, 0)

    def open_can(self):
        self.opened = True
        self.update_image()

    def close_can(self):
        self.opened = False
        self.update_image()

    def is_open(self):
        return self.opened
    
    def update_image(self):
        print(self.offset)
        if self.offset[0] == 0:
            self.change_offset((1,0))
            self.offset = (1,0)
        elif self.offset[0] == 1:
            self.change_offset((0,0))
            self.offset = (0,0)
        
    
    def update(self, seconds):
        super().update(seconds)

