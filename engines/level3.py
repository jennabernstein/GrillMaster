from .import GameEngine
import pygame

from gameObjects import *

from shapely.geometry import Polygon
import math

from utils import vec, RESOLUTION
import numpy as np
from FSMs import LevelProgressFSM


class GameEngine3(GameEngine):
    import pygame

    def __init__(self):       
        # initialize all drawable items
        self.chef = Chef((300,300))
        self.size = vec(*RESOLUTION)
        self.background = Drawable((0,0), "kitchen background.png")
        self.pinkCounter = Drawable((500,150), "pink counter.png")
        self.pinkPrep = Drawable((0, 425), "pink prep.png")
        self.longPinkCounter = Drawable((-120, 70), "pink long counter.png")
        self.customerCounter = Drawable((250, 325), "pink long counter.png")
        self.trash = Trash((455, 100), (0,0))
        self.patties1 = Patties((220, 185), (0,0))
        self.patties2 = Patties((175, 210), (1, 0))
        self.buns = Buns((130, 240))
        self.tomatoes = Tomatoes((270,160))
        self.lettuces = Lettuces((320, 130))
        self.cheeses = Cheeses((360, 100))
        self.hotdogmeat_plate = HotDog((70, 260))
        self.hotdogmeat_plate.scale((70,60))
        self.hotdogbun_plate = HotDogBuns((20, 290))
        self.hotdogbun_plate.scale((70,60))
        self.cola_machine = ColaMachine((780,250))
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
        self.foodList = [self.patties1, self.patties2, self.trash, self.tomatoes, self.lettuces, self.cheeses, self.buns, self.hotdogmeat_plate, self.hotdogbun_plate]
        self.cookStations = [self.cookStation]
        self.burger_images = [None, None, None]
        self.hotdog_images = [None, None, None]
        self.burger_state = None
        self.burger_meal = None
        self.patty_image = None
        self.hotdog_image = None
        self.hotdog_state = None
        self.currently_cooking = []
        self.level = 2
        self.customerManager = CustomerManager(self.level)
        self.customer_queue = self.customerManager.get_queue()

        self.serving_station1 = ServingStation([(380,600), (450,650), (575,575), (500,525)])
        self.servingPlate1 = Drawable((455,565), "food/plate.png", (0,0), 0.3)
        self.serving_station2 = ServingStation([(575,575), (500,525), (630, 450), (710, 500)])
        self.servingPlate2 = Drawable((560,500), "food/plate.png", (0,0), 0.3)
        self.serving_station3 = ServingStation([(630, 450), (710, 500), (825,435), (755,380)])
        self.servingPlate3 = Drawable((675,435), "food/plate.png", (0,0), 0.3)
        self.serving_stations = [self.serving_station1, self.serving_station2, self.serving_station3]
        self.customerManager.stations = self.serving_stations
        self.meal_images = [None, None, None]
        self.meals = [None, None, None]

        self.customers = [None, None, None]
        self.tickets = [None, None, None]
        self.ticket_position1 = (580,5)
        self.ticket_position2 = (690, 5)
        self.ticket_position3 = (800, 5)
        self.ticket_positions = [self.ticket_position1, self.ticket_position2, self.ticket_position3]

        self.current_patty_offset = 0
        self.tickets_created = []
        self.customer_spawn_interval = 10  
        self.last_order_fulfilled_time = 0
        self.current_level = 2
        self.customer_times = [3,25,40,65,80,95,105]
        self.times_used = []
        self.new_ticket_position = None


        self.gameClock = pygame.time.Clock()
        self.gameTime = 0
        self.timer = 0
        self.initialTime = 0

        self.dragged_ticket = None
        self.dragged_ticket_initial_position = None
        self.dragged_ticket_position = None
        self.dragged_cola_initial_position = None
        self.dragged_name_initial_position = None
        self.dragging = False

        self.loaded = False

        self.score = 0
        self.score_to_complete = 900
        self.customers_served = []
        self.customers_spawned = 0
        self.customers_done = []
        self.customers_to_serve = 7
        self.gameOver = False
        self.customers_next = []
        self.meals_done = []

        self.draw_cola = [False, False, False]
        self.cola_pictures = [None, None, None]

    def scaleDrawable(self, drawable, new_size):
        # scale size of drawable item
        scaled_image = pygame.transform.scale(drawable.image, new_size)
        scaled_drawable = Drawable(drawable.position, "")
        scaled_drawable.image = scaled_image
        return scaled_drawable
    

    def draw(self, drawSurface):      
        #draw background and ingredients   
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
        self.hotdogmeat_plate.draw(drawSurface)
        self.buns.draw(drawSurface)
        self.hotdogbun_plate.draw(drawSurface)
        for burger_image in self.burger_images:
            if burger_image is not None:
                burger_image.draw(drawSurface)
        for hotdog_image in self.hotdog_images:
            if hotdog_image is not None:
                hotdog_image.draw(drawSurface)
        self.chef.draw(drawSurface)
        if self.chef.isHoldingItem():
            self.chef.item.draw(drawSurface)
        self.pinkPrep.draw(drawSurface)
        self.customerCounter.draw(drawSurface)
        if self.patty_image:
            self.patty_image.draw(drawSurface)
        if self.hotdog_image:
            self.hotdog_image.draw(drawSurface)
        for station in self.currently_cooking:
            if self.patty_image:
                percentage = station.pattyFSM.get_cooking_percentage()
            else:
                percentage = station.hotdogFSM.get_cooking_percentage()
            position = (station.centroid[0] -40, station.centroid[1] + 30)
            self.draw_timer(drawSurface, position, 10, percentage)
        self.servingPlate1.draw(drawSurface)
        self.servingPlate2.draw(drawSurface)
        self.servingPlate3.draw(drawSurface)

        self.menu_instructions = TextEntry((5,5), "Press m to return to main menu", "default10")
        self.menu_instructions.draw(drawSurface)
        self.score_display = TextEntry((5,25), "Score: " + self.getScore() + "/900", "default15")
        self.score_display.draw(drawSurface)
        self.customer_display = TextEntry((5,45), "Customers Remaining: " + str(self.customers_to_serve - self.customers_spawned), "default15")
        self.customer_display.draw(drawSurface)

        image = self.cola_machine.colaMachineFSM.getStateImage(self.cola_machine.position)
        image.draw(drawSurface)
        
        for plate in self.meal_images:
            if plate is not None:
                plate.draw(drawSurface)
                    
        # make cola drawable if needed
        for i in range(len(self.draw_cola)):
            if self.draw_cola[i]:
                if i == 0:
                    position = self.serving_stations[i].centroid.x-10, self.serving_stations[i].centroid.y - 90
                elif i in [1,2]:
                    position = self.serving_stations[i].centroid.x-25, self.serving_stations[i].centroid.y - 80
                cola =  Drawable(position, "food/cola.png")
                cola.scale((100,100))
                cola.stateType = 'cola'
                self.cola_pictures[i] = cola
        
        # draw cola on station
        for c in self.cola_pictures:
            if c is not None:
                c.draw(drawSurface)

        # draw customer with name
        for i in range(len(self.tickets)):
            if self.tickets[i] is not None:
                customer = self.customers[i]
                if self.tickets[i].image is not None:
                    self.tickets[i].image.draw(drawSurface)
                self.tickets[i].customerName.draw(drawSurface)
                if 'cola' in self.tickets[i].ticketItems:
                    self.tickets[i].cola.draw(drawSurface)        

        # draw tickets with customer name, and cola if necessary
        for customer in self.customer_queue:
            if customer is not None:
                customer.draw(drawSurface)
                customerName = TextEntry((customer.timer_position[0]+10,customer.timer_position[1]+20), customer.name, "default10")
                customer_percentage = customer.get_patience_percentage()
                self.draw_customer_timer(drawSurface, customer.timer_position, 10, customer_percentage)
                customerName.draw(drawSurface)
            if customer is None:
                index = self.customer_queue.index(customer)
                if self.tickets[index] is not None:
                    self.tickets[index] = None
            

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
            self.handle_ticket_fulfillment_event(event, new_position)
            #handle cola machine event
            self.handle_cola_event(new_position)
        else:
            if event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
                # handle dragging and fulfilling the ticket
                self.handle_ticket_fulfillment_event(event, event.pos)
           
    def getScore(self):
        return str(self.score)

    def handle_foodlist_event(self, new_position):
        # for each item of food (and the trash can)
        for i in self.foodList:
            # if item i was the one that was clicked on
            if i.collide(new_position):
                # move chef to the position specified by the item
                self.chef.move((i.position[0] + i.chefPos[0], i.position[1] + i.chefPos[1]))
                if i != self.trash:
                    self.trash.close_can()
                direction = np.array(self.chef.position) - (i.position[0] + i.chefPos[0], i.position[1] + i.chefPos[1])
                distance = np.linalg.norm(direction)
                # can only complete pick up/drop off if within distance of 5
                if distance < 5:
                    if i == self.trash:
                        # throw away item
                        self.trash.open_can()
                        self.chef.dropOff()
                        self.score -= 35
                    else:
                        # pick up item
                        self.trash.close_can()
                        self.chef.pickUp(i.item)

    def handle_mealprepstation_event(self, new_position):
        # for each meal prep station
        for x in self.mealPrepStations:
            # if x was the clicked on station
            if x.collide(new_position):
                # move chef to station
                self.chef.move(x.chefPos)

            direction = np.array(self.chef.position) - x.chefPos
            distance = np.linalg.norm(direction)

            # if not already holding an item and distance within 5
            if not self.chef.isHoldingItem() and x.collide(new_position):
                if distance < 5:
                    # if the burger is ready to be picked up (meaning it has a cooked patty on it)
                    if x.burgerFSM.is_burger_ready():
                        index = self.mealPrepStations.index(x)
                        self.chef.pickUp(self.burger_images[index])
                        self.burger_state = x.burgerFSM.current_state
                        self.burger_meal = x.burgerFSM.meal
                        self.burger_images[index] = None
                        x.burgerFSM.reset()
                    # if the hot dog is ready to be picked up (meaning it has a cooked hot dog on it)
                    if x.hotdogMealFSM.is_hotdog_ready():
                        index = self.mealPrepStations.index(x)
                        self.chef.pickUp(self.hotdog_images[index])
                        self.hotdog_state = x.hotdogMealFSM.current_state
                        self.hotdog_meal = x.hotdogMealFSM.meal
                        self.hotdog_images[index] = None
                        x.hotdogMealFSM.reset()

            # if chef is holding an item (meaning they want to drop it off) and they're within a distance of 5
            elif self.chef.isHoldingItem() and x.collide(new_position):
                if distance < 5:
                    itemType = self.chef.item.getStateType()
                    # build meal based on what the chef was holding
                    if itemType not in x.burgerFSM.meal:
                        if (itemType == 'bun') or ((itemType == 'cooked meat patty' or itemType == 'cooked vegan patty') and 'bun' in x.burgerFSM.meal and ('cooked meat patty' not in x.burgerFSM.meal or 'cooked vegan patty' not in x.burgerFSM.meal)) or ((itemType == 'lettuce' or itemType == 'tomato' or itemType == 'cheese') and ('bun' in x.burgerFSM.meal)):
                            self.chef.dropOff()
                            x.burgerFSM.updateBurger(itemType)
                            index = self.mealPrepStations.index(x)
                            self.burger_images[index] = x.burgerFSM.getStateImage((x.centroid[0]-35, x.centroid[1]-42))
                        # if holding an already made burger
                        elif itemType.split()[0] == 'burger':
                            self.chef.dropOff()
                            x.burgerFSM.set_current_state(self.burger_state, self.burger_meal)
                            self.burger_state = None
                            self.burger_meal = None
                            index = self.mealPrepStations.index(x)
                            self.burger_images[index] = x.burgerFSM.getStateImage((x.centroid[0]-35, x.centroid[1]-42))
                    if itemType not in x.hotdogMealFSM.meal:
                        if itemType == 'hot dog bun' or itemType == 'cooked hot dog meat':
                            self.chef.dropOff()
                            x.hotdogMealFSM.updateHotDog(itemType)
                            index = self.mealPrepStations.index(x)
                            self.hotdog_images[index] = x.hotdogMealFSM.getStateImage((x.centroid[0]-35, x.centroid[1]-30))
                        # if holding an already completed hot dog meal
                        elif itemType == 'hot dog meal':
                            self.chef.dropOff()
                            x.hotdogMealFSM.set_current_state(self.hotdog_state, self.hotdog_meal)
                            self.hotdog_state = None
                            self.hotdog_meal = None
                            index = self.mealPrepStations.index(x)
                            self.hotdog_images[index] = x.hotdogMealFSM.getStateImage((x.centroid[0]-35, x.centroid[1]-30))


    def handle_cookstation_event(self, new_position):
        # for each cookstation (grill)
        for y in self.cookStations:
            if y.collide(new_position):
                self.chef.move(y.chefPos)
            direction = np.array(self.chef.position) - y.chefPos
            distance = np.linalg.norm(direction)
            if distance < 5:
                    if self.chef.isHoldingItem():
                        itemType = self.chef.item.getStateType()
                        # if the chef is holding a patty, drop off and update the patty fsm
                        if (itemType == 'vegan patty' or itemType == 'meat patty') and not (y.isHotDogOn() or y.isPattyOn()):
                            if y not in self.currently_cooking:
                                self.currently_cooking.append(y)
                            self.current_patty_offset = self.chef.item.offset
                            self.patty_image = y.pattyFSM.getStateImage((y.centroid[0]-20, y.centroid[1]-10), self.current_patty_offset)
                            self.chef.dropOff()
                            y.pattyOn = True
                            self.timer = 0
                        # if chef is holding a hot dog, drop off and update the hot dog fsm
                        elif itemType == 'hot dog meat' and not (y.isHotDogOn() or y.isPattyOn()):
                            if y not in self.currently_cooking:
                                self.currently_cooking.append(y)
                            self.hotdog_image = y.hotdogFSM.getStateImage((y.centroid[0]-35, y.centroid[1]-10))
                            self.chef.dropOff()
                            y.hotdogOn = True
                            self.timer = 0


    def handle_cooking(self, new_position):
        # for each cookstation that is currently cooking
        if len(self.currently_cooking) >= 1:
            for j in self.currently_cooking:
                if j.collide(new_position):
                    direction = np.array(self.chef.position) - j.chefPos
                    distance = np.linalg.norm(direction)
                    if distance < 5:
                        # if the patty is done cooking, chef can pick it up
                        if j.pattyFSM.is_done_cooking() and not self.chef.isHoldingItem():
                            self.chef.pickUp(self.patty_image)
                            j.pattyOn = False
                            self.currently_cooking.remove(j)
                            j.pattyFSM.reset()
                            self.patty_image = None
                        # if hot dog is done cooking, chef can pick it up
                        if j.hotdogFSM.is_done_cooking() and not self.chef.isHoldingItem():
                            self.chef.pickUp(self.hotdog_image)
                            j.hotdogOn = False
                            self.currently_cooking.remove(j)
                            j.hotdogFSM.reset()
                            self.hotdog_image = None


    def handle_serving_meal(self, new_position):
        # for all the customer serving stations
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
                            # if the chef is holding a burger or hot dog, then update the meal fsm and image on the serving station
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
                                    w.mealFSM.position = position
                                    image = w.mealFSM.getStateImage(item, position)
                                    if image is not None:
                                        self.meal_images[a] = image
                                        self.meals[a] = item
                                w.mealFSM.updateMeal(item)
                                w.meal = w.mealFSM.getMeal()
                            elif itemType == 'hot dog meal':
                                item = self.chef.item
                                self.chef.dropOff()
                                if self.meal_images[a] == None:
                                    if a == 0:
                                        position = (self.servingPlate1.position[0]-10, self.servingPlate1.position[1]-10)
                                    elif a == 1:
                                        position = (self.servingPlate2.position[0]-10, self.servingPlate2.position[1]-10)
                                    else:
                                        position = (self.servingPlate3.position[0]-10, self.servingPlate3.position[1]-10)
                                    w.mealFSM.position = position
                                    image = w.mealFSM.getStateImage(item, position)
                                    if image is not None:
                                        self.meal_images[a] = image
                                        self.meals[a] = item
                                w.mealFSM.updateMeal(item)
                                w.meal = w.mealFSM.getMeal()
                            # if item is a soda can, then add that to meal fsm
                            elif itemType == 'cola' and 'cola' not in w.mealFSM.meal:
                                item = self.chef.item
                                w.meal = w.mealFSM.getMeal()
                                w.mealFSM.meal.append(item.stateType)
                                self.draw_cola[a] = True
                                self.chef.dropOff()
                    # pick meal back up if chef isn't holding an item already, so that it can be moved to a different serving station or thrown in trash if needed
                    elif not self.chef.isHoldingItem():
                        if self.meals[a] is not None:
                            self.chef.pickUp(self.meals[a])
                            self.meal_images[a] = None
                            self.meals[a] = None
                            w.mealFSM.reset()
                        # can only pick up the soda can if it is the only thing on the serving station
                        elif self.draw_cola[a] and w.mealFSM.meal == ['cola']:
                            self.chef.pickUp(self.cola_machine.item)
                            self.serving_stations[a].meal = []
                            w.mealFSM.meal = []
                            self.cola_pictures[a] = None
                            self.draw_cola[a] = False


    def handle_ticket_fulfillment_event(self, event, new_position):
        event_type = event.type
        # if clicking on the ticket
        if event_type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(self.tickets)):
                ticket = self.tickets[i]
                if ticket is not None:
                    if ticket.image.rect.collidepoint(new_position):
                        # Start dragging the ticket
                        self.dragged_ticket_initial_position = ticket.image.position
                        self.dragged_ticketRect_initial_position = (ticket.image.rect.left, ticket.image.rect.top)
                        self.dragged_cola_initial_position = ticket.cola.position
                        self.dragged_name_initial_position = ticket.customerName.position
                        ticket.dragging = True
                        cola = ticket.cola
                        cola.position = (ticket.image.position[0]+45,ticket.image.position[1]-10)
                        customerName = ticket.customerName
                        customerName.position = (ticket.image.position[0]+10,ticket.image.position[1]+25)
                        ticket.name = self.customers[i].name
        if event_type == pygame.MOUSEMOTION:
            # Update the position of the dragged ticket
            for i in range(len(self.tickets)):
                ticket = self.tickets[i]
                if ticket is not None:
                    if ticket.dragging:
                        ticket.image.position = new_position[0]-50, new_position[1]-50
                        ticket.updateRectPosition((new_position[0]-50, new_position[1]-50))
                        cola = ticket.cola
                        cola.position = (ticket.image.position[0]+45,ticket.image.position[1]-10)
                        customerName = ticket.customerName
                        customerName.position = (ticket.image.position[0]+10,ticket.image.position[1]+25)
                        ticket.name = self.customers[i].name
        elif event_type == pygame.MOUSEBUTTONUP:
            for ticket in self.tickets:
                if ticket is not None:
                    if ticket.dragging:
                        # Check if the dragged ticket is dropped onto a serving station
                        for serving_station in self.serving_stations:
                            if serving_station.rectangles_collide(ticket.image.rect) or serving_station.collide(new_position):
                                if serving_station.customer is not None:
                                    if sorted(serving_station.meal) == sorted(ticket.ticketItems) and serving_station.customer.name == ticket.name:
                                        # Fulfill the order by updating the meal FSM to the serve state
                                        serving_station.mealFSM.updateMeal(ticket)
                                        serving_station.mealFSM.reset()
                                        station_index = self.serving_stations.index(serving_station)
                                        self.meal_images[station_index] = serving_station.mealFSM.getStateImage(None, serving_station.mealFSM.position)
                                        serving_station.meal = serving_station.mealFSM.getMeal()
                                        self.ticket_dragged = True
                                        # Clear the ticket
                                        index = self.tickets.index(ticket)
                                        self.tickets[index] = None
                                        self.customer_queue[index].order.filled = True
                                        self.score += serving_station.customer.getScore()
                                        self.customers_served.append(serving_station.customer)
                                        self.current_time = self.gameTime
                                        self.draw_cola[station_index] = False
                                        self.cola_pictures[station_index] = None
                        # reset positions if wrong meal or not overlapping with a meal
                        ticket.image.position = self.dragged_ticket_initial_position
                        ticket.updateRectPosition(self.dragged_ticketRect_initial_position)
                        ticket.cola.position = self.dragged_cola_initial_position
                        ticket.customerName.position = self.dragged_name_initial_position
                        ticket.dragging = False


    def handle_cola_event(self, new_position):
        # update the cola machine fsm and image based on time
        if self.cola_machine.collide(new_position):
                self.chef.move(self.cola_machine.chefPos)
        direction = np.array(self.chef.position) - self.cola_machine.chefPos
        distance = np.linalg.norm(direction)
        if distance < 5:
            if self.cola_machine.collide(new_position):
                if not self.chef.isHoldingItem():
                    if self.cola_machine.colaMachineFSM.current_state_value in ['one_can', 'two_cans', 'three_cans']:
                        self.chef.pickUp(self.cola_machine.item)
                        if self.cola_machine.colaMachineFSM.current_state_value == 'one_can':
                            self.cola_machine.time = 0
                        elif self.cola_machine.colaMachineFSM.current_state_value == 'two_cans':
                            self.cola_machine.time = 15
                        elif self.cola_machine.colaMachineFSM.current_state_value == 'three_cans':
                            self.cola_machine.time = 30
                        # pick up a can
                        self.cola_machine.colaMachineFSM.takeCan()



    def get_unused_ticket_position(self):
        # get the first ticket position that is unused
        positions = [self.ticket_position1, self.ticket_position2]
        unused_positions = set(positions) - self.used_positions
        return next(iter(unused_positions), None)
    
    def getGameOver(self):
        # return if the game is over, the final score, and the score that was needed
        return ([self.gameOver, self.score, self.score_to_complete])
    
    def passed(self):
        # return if they passed the level or not, based on their score
        return self.score >= self.score_to_complete

    def update(self, seconds):
        # update all the timers
        self.gameTime += seconds
        self.cola_machine.time += seconds   
         # get the customer queue           
        self.customer_queue = self.customerManager.get_queue()
        self.customers_done = self.customerManager.get_customers_done()
        for x in self.customer_queue:
            if x is not None:
                x.decreasePatience(seconds)
                x.update(seconds)
        # update chef sprite
        self.chef.update(seconds)
        Drawable.updateOffset(self.chef, self.size)
        if self.chef.isHoldingItem() and (self.chef.item.getStateType() == 'cooked meat patty' or self.chef.item.getStateType() == 'cooked meat patty'):
            self.patty_image = None
        # add new customer if there is a free station
        if self.is_time_to_spawn_customer():
            freeStation = False
            for i in self.serving_stations:
                if i.customer == None:
                    freeStation = True
            if freeStation == True:
                self.spawn_customer()
            elif freeStation == False:
                self.customers_next.append(self.spawn_customer())
        if len(self.customers_next) >= 1:
            freeStation = False
            for i in self.serving_stations:
                if i.customer == None:
                    freeStation = True
            if freeStation == True:
                self.spawn_customer(self.customers_next[0])
                self.customers_next.remove(self.customers_next[0])
        # Update the cooking process
        self.update_cooking(seconds)
        # Update the meal prep stations
        self.update_meal_prep_stations()    
        # update the customer queue   
        self.customerManager.update_timer(seconds)
        self.customerManager.update_queue(seconds)
        # update cola machine fsm
        if self.cola_machine.time //15 == 1 and self.cola_machine.colaMachineFSM.current_state_value == 'empty':
            self.cola_machine.colaMachineFSM.update_machine()
        if self.cola_machine.time //15 == 2 and self.cola_machine.colaMachineFSM.current_state_value == 'one_can':
            self.cola_machine.colaMachineFSM.update_machine()
        if self.cola_machine.time //15 >= 3 and self.cola_machine.colaMachineFSM.current_state_value in ['two_cans', 'three_cans']:
            self.cola_machine.colaMachineFSM.update_machine()

        # check if game over
        if len(self.customers_done) >= self.customers_to_serve:
            self.gameOver = True



    def update_cooking(self, seconds):
        # update the timer and the fsm for the hot dog or patty for cooking
        if len(self.currently_cooking) >= 1:
            self.timer += seconds
            for i in self.currently_cooking:
                if self.patty_image is not None:
                    i.pattyFSM.update_cooking(self.timer)
                    self.patty_image = i.pattyFSM.getStateImage((i.centroid[0] - 20, i.centroid[1] - 10), self.current_patty_offset)
                elif self.hotdog_image is not None:
                    i.hotdogFSM.update_cooking(self.timer)
                    self.hotdog_image = i.hotdogFSM.getStateImage((i.centroid[0] - 35, i.centroid[1] - 10))

    def update_meal_prep_stations(self):
        # update image of the burger fsm on the meal prep station
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
            # draw a red circle since it is burnt
            pygame.draw.circle(drawSurface, (255, 0, 0), position, radius)
    
    def draw_customer_timer(self, drawSurface, position, radius, percentage):
        # draw the timer for the customer for their patience level
        pygame.draw.circle(drawSurface, (0, 0, 0), position, radius)
        if 0 < percentage < 1:
            self.draw_arc(drawSurface, position, radius, percentage, (0, 255, 0))

    def draw_arc(self, drawSurface, position, radius, percentage, color):
        # draw the arc for the percentage left
        angle = 360 * percentage
        pygame.draw.arc(drawSurface, color, (position[0] - radius, position[1] - radius, 2 * radius, 2 * radius), math.radians(-90), math.radians(-90 + angle), width=6)


    def spawn_customer(self, new_customer=None):
        # spawn customer based on a the current level and the types of meals that have already been done
        self.customers_spawned += 1
        if new_customer is None:
            new_customer = self.customerManager.add_person()
        else:
            new_customer = new_customer
        if self.tickets[0] == None:
            new_customer.order.generateOrderLevel3(self.ticket_position1, self.meals_done)
            self.tickets[0] = new_customer.order
            if 'cooked meat patty' in self.tickets[0].ticketItems or 'cooked vegan patty' in self.tickets[0].ticketItems:
                HDorB = 'burger'
            elif 'hot dog meal' in self.tickets[0].ticketItems:
                HDorB = 'hot dog'
            if 'cola' in self.tickets[0].ticketItems:
                cola = 'True'
            else:
                cola = 'False'
            self.meals_done.append([HDorB,cola])
            self.customers[0] = new_customer
        elif self.tickets[1] == None:
            new_customer.order.generateOrderLevel3(self.ticket_position2, self.meals_done)
            self.tickets[1] = new_customer.order
            HDorB = 'hot dog'
            cola = 'False'
            if 'cooked meat patty' in self.tickets[1].ticketItems or 'cooked vegan patty' in self.tickets[1].ticketItems:
                HDorB = 'burger'
            elif 'hot dog meal' in self.tickets[1].ticketItems:
                HDorB = 'hot dog'
            if 'cola' in self.tickets[1].ticketItems:
                cola = 'True'
            else:
                cola = 'False'
            self.meals_done.append([HDorB,cola])
            self.customers[1] = new_customer
        elif self.tickets[2] == None:
            new_customer.order.generateOrderLevel3(self.ticket_position3, self.meals_done)
            self.tickets[2] = new_customer.order
            HDorB = 'hot dog'
            cola = 'False'
            if 'cooked meat patty' in self.tickets[2].ticketItems or 'cooked vegan patty' in self.tickets[2].ticketItems:
                HDorB = 'burger'
            elif 'hot dog meal' in self.tickets[2].ticketItems:
                HDorB = 'hot dog'
            if 'cola' in self.tickets[2].ticketItems:
                cola = 'True'
            else:
                cola = 'False'
            self.meals_done.append([HDorB,cola])
            self.customers[2] = new_customer 
        return new_customer


    def is_time_to_spawn_customer(self):
        # check if it is time to spawn a new customer
        if int(self.gameTime) in self.customer_times and int(self.gameTime) not in self.times_used:
            self.times_used.append(int(self.gameTime))
            return True

    def fulfill_order(self, order):
        # Called when the player fulfills an order
        # if ticket is dragged to the order, then order is fulfilled
        self.last_order_fulfilled_time = self.gameTime
        index = self.tickets.index(order)
        self.tickets[index] = None
        self.customer_queue[index].order = None
        self.customer_queue[index].order.filled = True