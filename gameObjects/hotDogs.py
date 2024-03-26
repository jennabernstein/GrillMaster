from . import Drawable
import pygame
from FSMs import HotDogFSM

class HotDog(Drawable):
    def __init__(self, position, scale=0.3):
        super().__init__(position, "food/hot dog/hot dog plate.png", (0,0), scale)
        self.chefPos = (20, 0)
        self.item = Drawable(position, "food/hot dog/hot dog meat.png")
        self.item.scale((60,20))
        self.hotdogFSM = HotDogFSM(self)
        self.item.stateType = 'hot dog meat'
    
    def update(self, seconds):
        super().update(seconds)

    def getStateType(self):
        return self.item.stateType