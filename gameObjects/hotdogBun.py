from . import Drawable
import pygame

class HotDogBuns(Drawable):
    def __init__(self, position, scale=0.3):
        super().__init__(position, "food/hot dog/hot dog bun plate.png", (0,0), scale)
        self.nFrames = 1
        self.chefPos = (20, -20)
        self.item = Drawable(position, "food/hot dog/hot dog bun.png")       
        self.item.scale((60,30))
        self.item.stateType = 'hot dog bun'
    
    def update(self, seconds):
        super().update(seconds)

    def getStateType(self):
        return self.item.stateType