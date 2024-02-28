from . import Drawable
import pygame

class Patties(Drawable):
    def __init__(self, position, offset, scale=0.5):
        super().__init__(position, "food/patty.png", offset, scale)
        self.nFrames = 2
    
    def update(self, seconds):
        super().update(seconds)



