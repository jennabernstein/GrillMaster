import pygame

from gameObjects import *

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
        self.plate1 = Drawable((540,170), "food/plate.png", (0,0), 0.3)
        self.orderPrepStation2 = MealPrepStation([(575,235), (640,200), (710,240), (650,280)])
        self.plate2 = Drawable((620,220), "food/plate.png", (0,0), 0.3)
        self.orderPrepStation3 = MealPrepStation([(710,240), (650,280), (740,330), (790,290)])
        self.plate3 = Drawable((700,265), "food/plate.png", (0,0), 0.3)
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

        self.serving_station1 = ServingStation([(380,600), (450,650), (575,575), (500,525)])
        self.servingPlate1 = Drawable((455,565), "food/plate.png", (0,0), 0.3)
        self.serving_station2 = ServingStation([(575,575), (500,525), (630, 450), (710, 500)])
        self.servingPlate2 = Drawable((560,500), "food/plate.png", (0,0), 0.3)
        self.serving_station3 = ServingStation([(630, 450), (710, 500), (825,435), (755,380)])
        self.servingPlate3 = Drawable((675,435), "food/plate.png", (0,0), 0.3)
        self.serving_stations = [self.serving_station1, self.serving_station2, self.serving_station3]
        self.meal_images = [None, None, None]
        self.meals = [None, None, None]

        self.customers = [None, None, None]
        self.tickets = [None, None, None]
        self.ticket_position1 = (580,5)
        self.ticket_position2 = (690, 5)
        self.ticket_position3 = (800, 5)

        self.current_patty_offset = 0
        self.tickets_created = []
        self.customer_spawn_interval = 10  
        self.last_order_fulfilled_time = 0
        self.current_level = 1
        self.customer_times = [5,15,30,40,60,75,85]
        self.times_used = []


        self.gameClock = pygame.time.Clock()
        self.gameTime = 0
        self.timer = 0
        self.initialTime = 0
        

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
        if len(self.orderPrepStation1.meal) < 1:
            self.plate1.draw(drawSurface)
        if len(self.orderPrepStation2.meal) < 1:
            self.plate2.draw(drawSurface)
        if len(self.orderPrepStation3.meal) < 1:
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
            position = (station.centroid[0] -40, station.centroid[1] + 30)
            self.draw_timer(drawSurface, position, 10, percentage)
        self.servingPlate1.draw(drawSurface)
        self.servingPlate2.draw(drawSurface)
        self.servingPlate3.draw(drawSurface)
        
        for plate in self.meal_images:
            if plate is not None:
                plate.draw(drawSurface)

        for i in self.tickets:
            if i is not None:
                pygame.draw.rect(drawSurface, (255,0,0),i.image.rect)
                i.image.draw(drawSurface)
        
        


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
            #handle serving the meal
            self.handle_serving_meal(new_position)
            #handle fulfilling ticket order
            self.handle_ticket_fulfillment_event(event.type, new_position)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.handle_ticket_fulfillment_event(event.type, new_position)
                            
        

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

    def handle_mealprepstation_event(self, new_position):
        for x in self.mealPrepStations:
            if x.collide(new_position):
                self.chef.move(x.chefPos)

            direction = np.array(self.chef.position) - x.chefPos
            distance = np.linalg.norm(direction)

            if not self.chef.isHoldingItem() and x.collide(new_position):
                if distance < 5:
                    if x.burgerFSM.is_burger_ready():
                        index = self.mealPrepStations.index(x)
                        self.chef.pickUp(self.burger_images[index])
                        self.burger_images[index] = None
                        x.burgerFSM.reset()
            
            elif self.chef.isHoldingItem() and x.collide(new_position):
                if distance < 5:
                    itemType = self.chef.item.getStateType()
                    if itemType not in x.burgerFSM.meal:
                        if (itemType == 'bun') or ((itemType == 'cooked meat patty' or itemType == 'cooked vegan patty') and 'bun' in x.burgerFSM.meal and ('cooked meat patty' not in x.burgerFSM.meal or 'cooked vegan patty' not in x.burgerFSM.meal)) or ((itemType == 'lettuce' or itemType == 'tomato' or itemType == 'cheese') and ('cooked meat patty' in x.burgerFSM.meal or 'cooked vegan patty' in x.burgerFSM.meal)):
                            self.chef.dropOff()
                            x.burgerFSM.updateBurger(itemType)
                            index = self.mealPrepStations.index(x)
                            self.burger_images[index] = x.burgerFSM.getStateImage((x.centroid[0]-35, x.centroid[1]-42))

    def handle_cookstation_event(self, new_position):
        for y in self.cookStations:
            if y.collide(new_position):
                self.chef.move(y.chefPos)
            direction = np.array(self.chef.position) - y.chefPos
            distance = np.linalg.norm(direction)
            if distance < 5:
                    if self.chef.isHoldingItem():
                        itemType = self.chef.item.getStateType()
                        if (itemType == 'vegan patty' or itemType == 'meat patty') and not y.isPattyOn():
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
                    direction = np.array(self.chef.position) - j.chefPos
                    distance = np.linalg.norm(direction)
                    if distance < 5:
                        if j.pattyFSM.is_done_cooking() and not self.chef.isHoldingItem():
                            self.chef.pickUp(self.patty_image)
                            j.pattyOn = False
                            self.currently_cooking.remove(j)
                            j.pattyFSM.reset()
                            self.patty_image = None


    def handle_serving_meal(self, new_position):
        for a in range(len(self.serving_stations)):
            w = self.serving_stations[a]
            if w.collide(new_position):
                self.chef.move(w.chefPos)
            direction = np.array(self.chef.position) - w.chefPos
            distance = np.linalg.norm(direction)
            if distance < 5:
                if w.collide(new_position):
                    if self.chef.isHoldingItem():
                            itemType = self.chef.item.getStateType()
                            if itemType.split()[0] == 'burger':
                                item = self.chef.item
                                self.chef.dropOff()
                                if self.meal_images[a] == None:
                                    if a == 0:
                                        position = (self.servingPlate1.position[0]-10, self.servingPlate1.position[1]-20)
                                    elif a == 1:
                                        position = (self.servingPlate2.position[0]-10, self.servingPlate2.position[1]-20)
                                    else:
                                        position = (self.servingPlate3.position[0]-10, self.servingPlate3.position[1]-20)

                                    image = w.mealFSM.getStateImage(item, position)
                                    if image is not None:
                                        self.meal_images[a] = image
                                        self.meals[a] = item
                                w.mealFSM.updateMeal(item)
                    elif not self.chef.isHoldingItem() and self.meals[a] is not None:
                        self.chef.pickUp(self.meals[a])
                        self.meal_images[a] = None
                        self.meals[a] = None
                        w.mealFSM.reset()

    def handle_ticket_fulfillment_event(self, event_type, new_position):
        if event_type == pygame.MOUSEBUTTONDOWN:
            for ticket in self.tickets:
                if ticket is not None:
                    if ticket.image.rect.collidepoint(new_position):
                        moving = True
        elif event_type == pygame.MOUSBUTTONUP:
            moving = False
            for a in range(len(self.serving_stations)):
                w = self.serving_stations[a]
                if w.collide(new_position):
                    pass



    def get_unused_ticket_position(self):
        positions = [self.ticket_position1, self.ticket_position2]
        unused_positions = set(positions) - self.used_positions
        return next(iter(unused_positions), None)

    def update(self, seconds):
        self.gameTime += seconds
        for x in self.customers:
            if x is not None:
                x.decreasePatience()
        self.chef.update(seconds)
        Drawable.updateOffset(self.chef, self.size)
        
        if self.chef.isHoldingItem() and (self.chef.item.getStateType() == 'cooked meat patty' or self.chef.item.getStateType() == 'cooked meat patty'):
            self.patty_image = None
        if self.is_time_to_spawn_customer():
            self.spawn_customer()
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
                self.burger_images[index] = j.burgerFSM.getStateImage((j.centroid[0] - 35, j.centroid[1] - 42))
    

    def draw_timer(self, drawSurface, position, radius, percentage):
        pygame.draw.circle(drawSurface, (0, 0, 0), position, radius)
        if 0 < percentage < 1:
            self.draw_arc(drawSurface, position, radius, percentage, (0, 255, 0))
        elif 1 <= percentage <= 1.5:
            # Clear the screen (draw a black circle)
            pygame.draw.circle(drawSurface, (0, 0, 0), position, radius)
            # Draw the second timer (percentage from 1 to 1.5)
            self.draw_arc(drawSurface, position, radius, max(0, percentage - 1)*2, (255, 255, 0))
        elif percentage > 1.5:
            pygame.draw.circle(drawSurface, (255, 0, 0), position, radius)


    def draw_arc(self, drawSurface, position, radius, percentage, color):
        angle = 360 * percentage
        pygame.draw.arc(drawSurface, color, (position[0] - radius, position[1] - radius, 2 * radius, 2 * radius), math.radians(-90), math.radians(-90 + angle), width=6)


    def spawn_customer(self):
        new_customer = Customer()
        new_customer.generateCustomerName()
        if self.tickets[0] == None:
            new_customer.order.generateOrder(self.ticket_position1)
            self.tickets[0] = new_customer.order
            self.customers[0] = new_customer
        elif self.tickets[1] == None:
            new_customer.order.generateOrder(self.ticket_position2)
            self.tickets[1] = new_customer.order
            self.customers[1] = new_customer
        elif self.tickets[2] == None:
            new_customer.order.generateOrder(self.ticket_position3)
            self.tickets[2] = new_customer.order
            self.customers[2] = new_customer

        # Adjust the time interval between customer arrivals based on the current level
        self.customer_spawn_interval = max(5, 15 - self.current_level)  


    def is_time_to_spawn_customer(self):

        if int(self.gameTime) in self.customer_times and int(self.gameTime) not in self.times_used:
            self.times_used.append(int(self.gameTime))
            return True

    def fulfill_order(self, order):
        # Called when the player fulfills an order
        self.last_order_fulfilled_time = self.gameTime
        index = self.tickets.index(order)
        self.tickets[index] = None
        # if ticket is dragged to the order, then order is fulfilled
        # check if ticket is same as what is given, then update mealFSM from burger to serve