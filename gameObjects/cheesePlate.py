from . import Drawable
import pygame

class Cheeses(Drawable):
    def __init__(self, position, scale=0.5):
        super().__init__(position, "food/lettuce and cheese.png", (1,0), scale)
        self.nFrames = 1
        self.chefPos = (20, 0)
        self.item = Drawable(position, "food/cheese.png")
        self.item.scale((50,50))
        self.item.stateType = 'cheese'
    
    def update(self, seconds):
        super().update(seconds)

    def getStateType(self):
        return self.stateType
