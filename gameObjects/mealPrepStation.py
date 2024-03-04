from . import Drawable
import pygame

class MealPrepStation(Drawable):
    def __init__(self, polygon):
        super().__init__()
        self.nFrames = 1
        self.chefPos = (20, 0)
        self.plate = None
        self.meal = []
        self.polygon = polygon
    
    def update(self, seconds):
        super().update(seconds)

    def collide(self,position):
        if position in self.polygon:
            return True


