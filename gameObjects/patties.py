from . import Drawable
import pygame

class Patties(Drawable):
    def __init__(self, position, offset, scale=0.5):
        super().__init__(position, "food/patties.png", offset, scale)
        self.nFrames = 2
        self.chefPos = (20, 0)
        if offset == (0,0):
            itemOffset = (0,0)
        elif offset == (1,0):
            itemOffset = (1,0)
        self.item = Drawable(position, "food/patty.png", itemOffset)
        self.item.scale((50,50))
    
    def update(self, seconds):
        super().update(seconds)

    def cook(self, seconds):
        pass



