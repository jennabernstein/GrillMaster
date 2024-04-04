from . import Drawable
from shapely.geometry import Polygon, Point
from FSMs.mealFSM import MealFSM

class ServingStation(Drawable):
    def __init__(self, polygon):
        super().__init__()
        self.nFrames = 1
        self.plate = None
        self.points = polygon
        self.polygon = Polygon(polygon)
        self.centroid = self.polygon.centroid
        self.chefPos = (self.centroid.x - 140, self.centroid.y - 140)
        self.mealFSM = MealFSM(self)
        self.meal = self.mealFSM.getMeal()
        self.customerPosition = (self.centroid.x + 15, self.centroid.y - 50)
        self.customer = None
    
    def rectangles_collide(self, rectangle):
        """
        Check if a rectangle collides with the serving station polygon.
        Rectangle is represented as a tuple (x, y, width, height).
        """
        rect_vertices = [(rectangle[0], rectangle[1]),
                        (rectangle[0] + rectangle[2], rectangle[1]),
                        (rectangle[0] + rectangle[2], rectangle[1] + rectangle[3]),
                        (rectangle[0], rectangle[1] + rectangle[3])]
        for vertex in rect_vertices:
            if self.collide(Point(vertex)):
                return True
        return False
    
    def update(self, seconds):
        super().update(seconds)
        self.meal = self.mealFSM.getMeal()


    def collide(self, position):
        """
        Check if a point (position) collides with the serving station polygon.
        """
        position = Point(position)
        return self.polygon.contains(position)
