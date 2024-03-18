from . import Drawable
import pygame
from shapely.geometry import Point, Polygon
from FSMs.mealFSM import MealFSM

class ServingStation(Drawable):
    def __init__(self, polygon):
        super().__init__()
        self.nFrames = 1
        self.plate = None
        self.points = polygon
        self.polygon = Polygon(polygon)
        self.centroid = (self.polygon.centroid.x, self.polygon.centroid.y)
        self.chefPos = (self.centroid[0] - 140, self.centroid[1] - 140)
        self.mealFSM = MealFSM(self)
        self.meal = self.mealFSM.getMeal()
    
    def update(self, seconds):
        super().update(seconds)
        self.meal = self.mealFSM.getMeal()

    def collide(self, position):
        position = Point(position)
        return self.polygon.contains(position)


