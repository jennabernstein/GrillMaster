from . import Drawable
import pygame

class Patties(Drawable):
    def __init__(self, position, offset, scale=0.5):
        super().__init__(position, "food/patties.png", offset, scale)
        self.nFrames = 2
        self.chefPos = (20, 0)
        self.item = Drawable(position, "food/patty.png", offset)
    
    def update(self, seconds):
        super().update(seconds)



