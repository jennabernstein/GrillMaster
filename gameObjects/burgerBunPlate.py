from . import Drawable
import pygame

class Bun(Drawable):
    def __init__(self, position, scale=0.5):
        super().__init__(position, "food/burger bun.png", (0,0), scale)
        self.nFrames = 1
        self.chefPos = (20, 0)
        self.item = Drawable(position, "food/burger bun.png")
        self.item.scale((50,50))
    
    def update(self, seconds):
        super().update(seconds)

