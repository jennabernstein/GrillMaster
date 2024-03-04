import pygame

from . import Drawable
from .chef import Chef
from .patties import Patties
from .trash import Trash
from .tomatoes import Tomatoes
from .lettucePlate import Lettuces
from .cheesePlate import Cheeses
from .onions import Onions
from .mealPrepStation import MealPrepStation
from .cookStation import CookStation

from shapely.geometry import Polygon

from utils import vec, RESOLUTION

class GameEngine(object):
    import pygame

    def __init__(self):       
        self.chef = Chef((300,300))
        self.size = vec(*RESOLUTION)
        self.background = Drawable((0,0), "kitchen background.png")
        self.pinkCounter = Drawable((500,150), "pink counter.png")
        self.pinkPrep = Drawable((0, 425), "pink prep.png")
        self.longPinkCounter = Drawable((-120, 70), "pink long counter.png")
        self.customerCounter = Drawable((250, 325), "pink long counter.png")
        self.trash = Trash((455, 100), (0,0))
        self.patties1 = Patties((100, 260), (0,0))
        self.patties2 = Patties((140, 230), (1, 0))
        self.tomatoes = Tomatoes((200, 200))
        self.onions = Onions((250, 175))
        self.lettuces = Lettuces((290, 150))
        self.cheeses = Cheeses((330, 120))
        self.orderPrepStation1 = MealPrepStation([(575,235), (640,200), (710,240), (650,280)])
        self.orderPrepStation2 = MealPrepStation([(575,235), (640,200), (560,150), (500,190)])
        self.orderPrepStation3 = MealPrepStation([(710,240), (650,280), (740,330), (790,290)])
        self.mealPrepStations = [self.orderPrepStation1,self.orderPrepStation2,self.orderPrepStation3]
        self.cookStation = CookStation([(20,470), (90,510), (150,480), (80,430)])
        self.pinkPrep = self.scaleDrawable(self.pinkPrep, (325, 300))
        self.pinkCounter = self.scaleDrawable(self.pinkCounter, (300, 250))
        self.longPinkCounter = self.scaleDrawable(self.longPinkCounter,(640, 375))
        self.customerCounter = self.scaleDrawable(self.customerCounter, (700, 420))
        self.foodList = [self.patties1, self.patties2, self.trash, self.tomatoes, self.onions, self.lettuces, self.cheeses]
        
        

    def scaleDrawable(self, drawable, new_size):
        scaled_image = pygame.transform.scale(drawable.image, new_size)
        scaled_drawable = Drawable(drawable.position, "")
        scaled_drawable.image = scaled_image

        return scaled_drawable
    
    def draw(self, drawSurface):        
        self.background.draw(drawSurface)
        self.longPinkCounter.draw(drawSurface)
        self.trash.draw(drawSurface)
        self.pinkCounter.draw(drawSurface)
        self.patties1.draw(drawSurface)
        self.patties2.draw(drawSurface)
        self.tomatoes.draw(drawSurface)
        self.cheeses.draw(drawSurface)
        self.onions.draw(drawSurface)
        self.lettuces.draw(drawSurface)
        self.chef.draw(drawSurface)
        if self.chef.isHoldingItem():
            self.chef.item.draw(drawSurface)
        self.pinkPrep.draw(drawSurface)
        self.customerCounter.draw(drawSurface)
        
        
            
    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            new_position = event.pos
            for i in self.foodList:
                if i.collide(new_position):
                    self.chef.move((i.position[0] + i.chefPos[0], i.position[1] + i.chefPos[1]))
                    if i == self.trash:
                        self.trash.open_can()
                        self.chef.dropOff()
                    else:
                        self.chef.pickUp(i.item)
            for x in self.mealPrepStations:
                if x.collide(new_position):
                    self.chef.move((x.position[0] + x.chefPos[0], x.position[1] + x.chefPos[1]))
                    if self.chef.isHoldingItem():
                        #if item is bread, drop off
                        #if item is cooked patty and there is bread there, drop off
                        #if item is topping and there is burger there and item is not already there, drop off
                        self.chef.dropOff()
        else:
            self.chef.handleEvent(event)


        self.trash.close_can()
    
    def update(self, seconds):
        self.chef.update(seconds)
        Drawable.updateOffset(self.chef, self.size)
