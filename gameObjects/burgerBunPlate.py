from . import Drawable
import pygame

class Buns(Drawable):
    def __init__(self, position, scale=0.2):
        super().__init__(position, "food/burger bun.png", (0,0), scale)
        self.nFrames = 1
        self.chefPos = (20, -20)
        self.item = Drawable(position, "food/burger/bun.png")       
        self.item.scale((50,50))
        self.item.stateType = 'bun'
    
    def update(self, seconds):
        super().update(seconds)

    def getStateType(self):
        return self.item.stateType