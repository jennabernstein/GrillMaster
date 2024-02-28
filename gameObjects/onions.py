from . import Drawable
import pygame

class Onions(Drawable):
    def __init__(self, position, scale=0.5):
        super().__init__(position, "food/onions.png", (0,0),scale)
        self.nFrames = 1
        self.chefPos = (20, 0)
        self.item = Drawable(position, "food/onion.png")
        self.item.scale((50,50))

    
    def update(self, seconds):
        super().update(seconds)


