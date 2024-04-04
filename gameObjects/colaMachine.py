from . import Drawable
from FSMs import ColaMachineFSM
import pygame

class ColaMachine(Drawable):
    def __init__(self, position, scale=.8):
        self.position = position
        self.scale = scale
        super().__init__(position, "cola machine.png", (0,0), scale)
        self.nFrames = 1
        self.chefPos = (650, 250)
        self.item = Drawable(position, "food/cola.png")
        self.item.scale((100,100))
        self.item.stateType = 'cola'
        self.time = 0
        self.colaMachineFSM = ColaMachineFSM(self)
    
    def update(self, seconds):
        super().update(seconds)

    def getStateType(self):
        return self.stateType
