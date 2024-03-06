from . import Drawable
import pygame
from FSMs.pattyFSM import PattyFSM

class Patties(Drawable):
    def __init__(self, position, offset, scale=0.5):
        super().__init__(position, "food/patties.png", offset, scale)
        self.chefPos = (20, 0)

        itemOffset = (offset[0], 0)
        self.item = Drawable(position, "food/burger sprites.png", itemOffset)
        self.item.offset = offset[0]
        self.item.scale((50,50))
        self.row = 0
        self.pattyFSM = PattyFSM(self)
        self.item.stateType = 'patty'
    
    def update(self, seconds):
        super().update(seconds)

    def getStateType(self):
        return self.item.stateType