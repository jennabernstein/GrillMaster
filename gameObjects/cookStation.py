from . import Drawable
import pygame
from shapely.geometry import Point, Polygon
from FSMs import PattyFSM, HotDogFSM

class CookStation(Drawable):
    def __init__(self, polygon):
        super().__init__()
        self.nFrames = 1
        self.chefPos = (20, 0)
        self.plate = None
        self.meal = []
        self.points = polygon
        self.polygon = Polygon(polygon)
        self.pattyOn = False
        self.hotdogOn = False
        self.centroid = (self.polygon.centroid.x, self.polygon.centroid.y)
        self.chefPos = (self.centroid[0] + 50, self.centroid[1]-120)
        self.pattyFSM = PattyFSM(self)
        self.hotdogFSM = HotDogFSM(self)
    
    def update(self, seconds):
        super().update(seconds)
        self.pattyFSM.update(seconds)

    def collide(self, position):
        position = Point(position)
        return self.polygon.contains(position)
    
    def isPattyOn(self):
        return self.pattyOn
    
    def isHotDogOn(self):
        return self.hotdogOn

    def cook(self, seconds):
        self.pattyFSM.update_cooking(seconds)

