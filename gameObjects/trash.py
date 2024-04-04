from .drawable import Drawable

class Trash(Drawable):
    def __init__(self, position, offset):
        super().__init__(position, "trash cans.png", offset)
        self.offset = offset
        self.nFrames = 2
        self.opened = False
        self.chefPos = (-20, 0)
        self.item = Drawable()
        self.item.stateType = 'trash'

    def open_can(self):
        self.opened = True
        self.update_image('open')

    def close_can(self):
        self.opened = False
        self.update_image('close')

    def is_open(self):
        return self.opened
    
    def update_image(self, command):
        if command == 'open':
            self.change_offset((1,0))
            self.offset = (1,0)
        elif command == 'close':
            self.change_offset((0,0))
            self.offset = (0,0)
        
    
    def update(self, seconds):
        super().update(seconds)

