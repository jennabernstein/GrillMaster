from . import Drawable
import pygame
from shapely.geometry import Point, Polygon
from FSMs.burgerFSM import BurgerFSM

class MealPrepStation(Drawable):
    def __init__(self, polygon):
        super().__init__()
        self.nFrames = 1
        self.plate = None
        self.meal = []
        self.points = polygon
        self.polygon = Polygon(polygon)
        self.centroid = (self.polygon.centroid.x, self.polygon.centroid.y)
        self.chefPos = (self.centroid[0] - 120, self.centroid[1] - 80)
        self.burgerFSM = BurgerFSM(self)
    
    def update(self, seconds):
        super().update(seconds)
        self.burgerFSM.update(seconds)

    def collide(self, position):
        position = Point(position)
        return self.polygon.contains(position)


