from . import Drawable
import pygame

class Tomatoes(Drawable):
    def __init__(self, position, scale=0.5):
        super().__init__(position, "food/tomatos.png", (0,0),scale)
        self.nFrames = 1
        self.chefPos = (20, 0)
        self.item = Drawable(position, "food/tomato.png")
        self.item.scale((50,50))
    
    def update(self, seconds):
        super().update(seconds)


