import pygame

from . import Drawable
from .chef import Chef
from .patties import Patties
from .trash import Trash
from .tomatoes import Tomatoes
from .lettucePlate import Lettuces
from .cheesePlate import Cheeses
from .mealPrepStation import MealPrepStation
from .cookStation import CookStation
from .burgerBunPlate import Buns

from shapely.geometry import Polygon
import math

from utils import vec, RESOLUTION
import numpy as np

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
        self.buns = Buns((30, 290))
        self.tomatoes = Tomatoes((200, 200))
        self.lettuces = Lettuces((290, 150))
        self.cheeses = Cheeses((330, 120))
        self.orderPrepStation1 = MealPrepStation([(575,235), (640,200), (560,150), (500,190)])
        self.plate1 = Drawable((530,160), "food/plate.png", (0,0), 0.4)
        self.orderPrepStation2 = MealPrepStation([(575,235), (640,200), (710,240), (650,280)])
        self.plate2 = Drawable((610,210), "food/plate.png", (0,0), 0.4)
        self.orderPrepStation3 = MealPrepStation([(710,240), (650,280), (740,330), (790,290)])
        self.plate3 = Drawable((690,255), "food/plate.png", (0,0), 0.4)
        self.mealPrepStations = [self.orderPrepStation1,self.orderPrepStation2,self.orderPrepStation3]
        self.cookStation = CookStation([(20,470), (90,510), (150,480), (80,430)])
        self.pinkPrep = self.scaleDrawable(self.pinkPrep, (325, 300))
        self.pinkCounter = self.scaleDrawable(self.pinkCounter, (300, 250))
        self.longPinkCounter = self.scaleDrawable(self.longPinkCounter,(640, 375))
        self.customerCounter = self.scaleDrawable(self.customerCounter, (700, 420))
        self.foodList = [self.patties1, self.patties2, self.trash, self.tomatoes, self.lettuces, self.cheeses, self.buns]
        self.cookStations = [self.cookStation]
        self.burger_images = [None, None, None]
        self.patty_image = None
        self.currently_cooking = []
        self.gameClock = pygame.time.Clock()
        self.gameTime = 0
        self.timer = 0
        self.initialTime = 0
        self.current_patty_offset = 0
        

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
        self.plate1.draw(drawSurface)
        self.plate2.draw(drawSurface)
        self.plate3.draw(drawSurface)
        self.patties1.draw(drawSurface)
        self.patties2.draw(drawSurface)
        self.tomatoes.draw(drawSurface)
        self.cheeses.draw(drawSurface)
        self.lettuces.draw(drawSurface)
        self.buns.draw(drawSurface)
        for burger_image in self.burger_images:
            if burger_image is not None:
                burger_image.draw(drawSurface)
        self.chef.draw(drawSurface)
        if self.chef.isHoldingItem():
            self.chef.item.draw(drawSurface)
        self.pinkPrep.draw(drawSurface)
        self.customerCounter.draw(drawSurface)
        if self.patty_image:
            self.patty_image.draw(drawSurface)
        for station in self.currently_cooking:
            percentage = station.pattyFSM.get_cooking_percentage()
            position = (station.centroid[0] - 20, station.centroid[1] - 30)
            self.draw_timer(drawSurface, position, 10, percentage)

        

        
            
    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            new_position = event.pos
            #handle picking up the food
            self.handle_foodlist_event(new_position)
            #handle prepping the food
            self.handle_mealprepstation_event(new_position)
            #handle cooking the patty
            self.handle_cookstation_event(new_position)
            #handle picking up a cooked patty
            self.handle_cooking(new_position)
                            
        

    def handle_foodlist_event(self, new_position):
        for i in self.foodList:
            if i.collide(new_position):
                self.chef.move((i.position[0] + i.chefPos[0], i.position[1] + i.chefPos[1]))
                if i != self.trash:
                    self.trash.close_can()
                direction = np.array(self.chef.position) - (i.position[0] + i.chefPos[0], i.position[1] + i.chefPos[1])
                distance = np.linalg.norm(direction)
                if distance < 5:
                    if i == self.trash:
                        self.trash.open_can()
                        self.chef.dropOff()
                    else:
                        self.trash.close_can()
                        self.chef.pickUp(i.item)
                        print(self.chef.holdingItem)

    def handle_mealprepstation_event(self, new_position):
        for x in self.mealPrepStations:
            if x.collide(new_position):
                self.chef.move(x.chefPos)
            direction = np.array(self.chef.position) - x.chefPos
            distance = np.linalg.norm(direction)
            if distance < 5:
                    if self.chef.isHoldingItem():
                        itemType = self.chef.item.getStateType()
                        if itemType not in x.burgerFSM.meal:
                            #if bun, if patty and bun is there and patty is not there, if topping and patty is there
                            if (itemType == 'bun') or (itemType == 'cooked patty' and 'bun' in x.burgerFSM.meal and 'cooked patty' not in x.burgerFSM.meal) or ((itemType == 'lettuce' or itemType == 'tomato' or itemType == 'cheese') and 'cooked patty' in x.burgerFSM.meal):
                                self.chef.dropOff()
                                x.burgerFSM.updateBurger(itemType)
                                index = self.mealPrepStations.index(x)
                                self.burger_images[index] = x.burgerFSM.getStateImage((x.centroid[0]-23, x.centroid[1]-35))
                    elif x.burgerFSM.is_burger_ready() and not self.chef.isHoldingItem():
                        index = self.mealPrepStations.index(x)
                        self.chef.pickUp(self.burger_images[index])
                        self.burger_images[index] = None
                        x.burgerFSM.reset()

    def handle_cookstation_event(self, new_position):
        for y in self.cookStations:
            if y.collide(new_position):
                self.chef.move(y.chefPos)
            direction = np.array(self.chef.position) - y.chefPos
            distance = np.linalg.norm(direction)
            if distance < 5:
                    if self.chef.isHoldingItem():
                        itemType = self.chef.item.getStateType()
                        if itemType == 'patty' and not y.isPattyOn():
                            if y not in self.currently_cooking:
                                self.currently_cooking.append(y)
                            self.current_patty_offset = self.chef.item.offset
                            self.patty_image = y.pattyFSM.getStateImage((y.centroid[0]-20, y.centroid[1]-10), self.current_patty_offset)
                            self.chef.dropOff()
                            y.pattyOn = True
                            self.timer = 0

    def handle_cooking(self, new_position):
        if len(self.currently_cooking) >= 1:
            for j in self.currently_cooking:
                if j.collide(new_position):
                    if j.pattyFSM.is_done_cooking():
                        self.chef.pickUp(self.patty_image)
                        j.pattyOn = False
                        self.currently_cooking.remove(j)
                        j.pattyFSM.reset()
                        self.patty_image = None



    def update(self, seconds):
        self.gameTime += seconds
        self.chef.update(seconds)
        Drawable.updateOffset(self.chef, self.size)
        
        if self.chef.isHoldingItem() and self.chef.item.getStateType() == 'cooked patty':
            self.patty_image = None

        # Update the cooking process
        self.update_cooking(seconds)

        # Update the meal prep stations
        self.update_meal_prep_stations()


    def update_cooking(self, seconds):
        if len(self.currently_cooking) >= 1:
            self.timer += seconds
            for i in self.currently_cooking:
                if self.patty_image is not None:
                    i.pattyFSM.update_cooking(self.timer)
                    self.patty_image = i.pattyFSM.getStateImage((i.centroid[0] - 20, i.centroid[1] - 10), self.current_patty_offset)

    def update_meal_prep_stations(self):
        for j in self.mealPrepStations:
            if j.burgerFSM.meal != []:
                index = self.mealPrepStations.index(j)
                self.burger_images[index] = j.burgerFSM.getStateImage((j.centroid[0] - 23, j.centroid[1] - 35))
    
    def draw_timer(self, drawSurface, position, radius, percentage):
        pygame.draw.circle(drawSurface, (0, 0, 0), position, radius)

        if 0 < percentage < 1:
            self.draw_arc(drawSurface, position, radius, percentage, (0, 200, 100))
        elif 1 <= percentage <= 1.5:
            # Clear the screen (draw a black circle)
            pygame.draw.circle(drawSurface, (0, 0, 0), position, radius)
            
            # Draw the second timer (percentage from 1 to 1.5)
            self.draw_arc(drawSurface, position, radius, max(0, percentage - 1)*2, (0, 200, 0))
        elif percentage > 1.5:
            pygame.draw.circle(drawSurface, (255, 0, 0), position, radius)

    def draw_arc(self, drawSurface, position, radius, percentage, color):
        angle = 360 * percentage
        pygame.draw.arc(drawSurface, color, (position[0] - radius, position[1] - radius, 2 * radius, 2 * radius), math.radians(-90), math.radians(-90 + angle), width=6)