from . import Drawable
import pygame

class Patties(Drawable):
    def __init__(self, position, offset):
        super().__init__(position, "food/patties.png", offset)
        self.nFrames = 2
        self.opened = False
        self.chefPos = (200, 200)
    
    def update(self, seconds):
        super().update(seconds)



