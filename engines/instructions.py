from .import GameEngine
import pygame

from gameObjects import *

from shapely.geometry import Polygon
import math
from pygame import font

from utils import vec, RESOLUTION
import numpy as np
from FSMs import LevelProgressFSM

class InstructionsEngine(GameEngine):
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
        self.level = 0
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
        self.times_used = []
        self.new_ticket_position = None


        self.gameClock = pygame.time.Clock()
        self.gameTime = 0
        self.timer = 0
        self.initialTime = 0
        self.current_time = 0

        self.dragged_ticket = None
        self.dragged_ticket_initial_position = None
        self.dragged_ticket_position = None
        self.dragged_cola_initial_position = None
        self.dragged_name_initial_position = None
        self.dragging = False

        self.loaded = False

        self.draw_cola = [False, False, False]
        self.cola_pictures = [None, None, None]


        self.score = 0
        self.score_to_complete = 0
        self.customers_served = []
        self.customers_done = []
        self.customer_times = [3]
        self.customers_to_serve = 3
        self.gameOver = False
        self.customers_next = []
        self.spawned = False
        self.welcome = TextEntry((10,5), "Welcome!", "default20", size = 20, color=(255,255,255))
        self.text = []
        self.completed_tickets = [False, False, False]

        self.pickedUpBun = False
        self.placed_bun = False
        self.cooking = False
        self.done_cooking = False
        self.meal_finished = False
        self.meal_served = False
        self.burnt = False
        self.ticket_dragged = False
        self.veganBurger_bun = False
        self.veganBurger_bun_placed = False
        self.veganBurger_meat_pickup = False
        self.veganBurger_meat_cooking = False
        self.veganBurger_meat_cooked = False
        self.veganBurger_meat_burnt = False
        self.veganBurger_meal_finished = False
        self.veganBurger_meal_served = False
        self.veganBurger_ticket_dragged = False
        self.meatBurger_bun = False
        self.meatBurger_bun_placed = False
        self.meatBurger_meat_pickup = False
        self.meatBurger_meat_cooking = False
        self.meatBurger_meat_cooked = False
        self.meatBurger_meat_burnt = False
        self.meatBurger_meal_finished = False
        self.meatBurger_meal_served = False
        self.meatBurger_ticket_dragged = False
        self.get_drink = False
        self.placed_drink = False

        self.meal1_done = False
        self.meal2_done = False
        self.meal3_done = False


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
        for customer in self.customer_queue:
            index = self.customer_queue.index(customer)
            if customer is not None:
                customer.draw(drawSurface)
                customerName = TextEntry((customer.timer_position[0]+10,customer.timer_position[1]+20), customer.name, "default10")
                customerName.draw(drawSurface)
            if customer is None:
                if self.tickets[index] is not None:
                    self.tickets[index] = None

        #for i in self.tickets:
        #    if i is not None:
        #        i.image.draw(drawSurface)

        # draw tickets with customer name, and cola if necessary
        for i in range(len(self.tickets)):
            if self.tickets[i] is not None:
                customer = self.customers[i]
                self.tickets[i].image.draw(drawSurface)
                self.tickets[i].customerName.draw(drawSurface)
                if 'cola' in self.tickets[i].ticketItems:
                    self.tickets[i].cola.draw(drawSurface)   

        #instructions to be displayed
        if self.spawned == True:
            if self.welcome is not None:
                self.welcome.draw(drawSurface)
            instruction_text1 = "You have your first customer!"
            instruction_text2 = "Their order shows up on the right."
            instruction_text3 = "Begin by clicking on and"
            instruction_text4 = "picking up the hot dog bun."
            instruction1 = TextEntry((5, 25), instruction_text1, "default15", size = 15, color=(255,255,255))
            instruction2 = TextEntry((5, 45), instruction_text2, "default15", size = 15, color=(255,255,255))
            instruction3 = TextEntry((5, 65), instruction_text3, "default15", size = 15, color=(255,255,255))
            instruction4 = TextEntry((5, 85), instruction_text4, "default15", size = 15, color=(255,255,255))
            self.text = [instruction1, instruction2, instruction3, instruction4]

        if self.pickedUpBun == True:
            self.welcome = None
            instruction_text1 = "Place the bun on one of the meal prep "
            instruction_text2 = "stations to the right to start"
            instruction_text3 = "building your meal."
            instruction1 = TextEntry((10, 5), instruction_text1, "default15", size = 15, color=(255,255,255) )
            instruction2 = TextEntry((10, 25), instruction_text2, "default15", size = 15, color=(255,255,255))
            instruction3 = TextEntry((10, 45), instruction_text3, "default15", size = 15, color=(255,255,255))
            self.text = [instruction1, instruction2, instruction3]

        if self.placed_bun:
            self.welcome = None
            instruction_text1 = "Now, click and pick up your hot dog"
            instruction_text2 = "and place it on the grill to cook."
            instruction1 = TextEntry((10, 5), instruction_text1, "default15", size = 15, color=(255,255,255))
            instruction2 = TextEntry((10, 25), instruction_text2, "default15", size = 15, color=(255,255,255))
            self.text = [instruction1, instruction2]

        if self.cooking:
            self.welcome = None
            instruction_text1 = "Once the hot dog timer reaches the "
            instruction_text2 = "yellow stage, it is ready!"
            instruction_text3 = "Don't leave it for too long or"
            instruction_text4 = "it will burn."
            instruction1 = TextEntry((10, 5), instruction_text1, "default15", size = 15, color=(255,255,255))
            instruction2 = TextEntry((10, 25), instruction_text2, "default15", size = 15, color=(255,255,255))
            instruction3 = TextEntry((10, 45), instruction_text3, "default15", size = 15, color=(255,255,255))
            instruction4 = TextEntry((10, 65), instruction_text4, "default15", size = 15, color=(255,255,255))
            self.text = [instruction1, instruction2, instruction3, instruction4]
        
        if self.done_cooking:
            instruction_text1 = "Pick up the hot dog and place it "
            instruction_text2 = "in the bun."
            instruction1 = TextEntry((10, 5), instruction_text1, "default15", size = 15, color=(255,255,255))
            instruction2 = TextEntry((10, 25), instruction_text2, "default15", size = 15, color=(255,255,255))
            self.text = [instruction1, instruction2]

        if self.burnt:
            instruction_text1 = "Oh no! The hot dog burned!"
            instruction_text2 = "Throw it away"
            instruction_text2 = "then cook a new one."
            instruction1 = TextEntry((10, 5), instruction_text1, "default15", size = 15, color=(255,255,255))
            instruction2 = TextEntry((10, 25), instruction_text2, "default15", size = 15, color=(255,255,255))
            instruction3 = TextEntry((10, 45), instruction_text3, "default15", size = 15, color=(255,255,255))
            self.text = [instruction1, instruction2, instruction3]

        if self.meal_finished:
            instruction_text1 = "Now that you have completed the meal,"
            instruction_text2 = "pick it up and place it on the"
            instruction_text3 = "plate in front of the customer."
            instruction1 = TextEntry((10, 5), instruction_text1, "default15", size = 15, color=(255,255,255))
            instruction2 = TextEntry((10, 25), instruction_text2, "default15", size = 15, color=(255,255,255))
            instruction3 = TextEntry((10, 45), instruction_text3, "default15", size = 15, color=(255,255,255))
            self.text = [instruction1, instruction2, instruction3]

        if self.meal_served:
            #serve the meal to the customer
            # and drag the ticket over the meal
            instruction_text1 = "In order to complete the meal, "
            instruction_text2 = "you must then drag the ticket "
            instruction_text3 = "over the completed meal."
            instruction1 = TextEntry((10, 5), instruction_text1, "default15", size = 15, color=(255,255,255))
            instruction2 = TextEntry((10, 25), instruction_text2, "default15", size = 15, color=(255,255,255))
            instruction3 = TextEntry((10, 45), instruction_text3, "default15", size = 15, color=(255,255,255))
            self.text = [instruction1, instruction2, instruction3]

        if self.ticket_dragged:
            instruction_text1 = "Nice job! Now let's try it with a"
            instruction_text2 = "burger. First, pick up the burger bun"
            instruction_text3 = "and place on the prep station."
            instruction1 = TextEntry((10, 5), instruction_text1, "default15", size = 15, color=(255,255,255))
            instruction2 = TextEntry((10, 25), instruction_text2, "default15", size = 15, color=(255,255,255))
            instruction3 = TextEntry((10, 45), instruction_text3, "default15", size = 15, color=(255,255,255))
            self.text = [instruction1, instruction2, instruction3]

        if self.veganBurger_bun_placed:
            instruction_text1 = "Now, click and pick up your burger"
            instruction_text2 = "patty and place it on the grill to"
            instruction_text3 = "cook. Pay attention to the type "
            instruction_text4 = "of patty."
            instruction1 = TextEntry((10, 5), instruction_text1, "default15", size = 15, color=(255,255,255))
            instruction2 = TextEntry((10, 25), instruction_text2, "default15", size = 15, color=(255,255,255))
            instruction3 = TextEntry((10, 45), instruction_text3, "default15", size = 15, color=(255,255,255))
            instruction4 = TextEntry((10, 65), instruction_text4, "default15", size = 15, color=(255,255,255))
            self.text = [instruction1, instruction2, instruction3, instruction4]

        if self.veganBurger_meat_cooked:
            instruction_text1 = "The patty is done cooking."
            instruction_text2 = "Pick up and place in burger."
            instruction1 = TextEntry((10, 5), instruction_text1, "default15", size = 15, color=(255,255,255))
            instruction2 = TextEntry((10, 25), instruction_text2, "default15", size = 15, color=(255,255,255))
            self.text = [instruction1, instruction2]

        if self.veganBurger_meat_burnt:
            instruction_text1 = "Oh no! Your patty burned!"
            instruction_text2 = "Throw away patty in trash"
            instruction_text3 = "and cook another."
            instruction1 = TextEntry((10, 5), instruction_text1, "default15", size = 15, color=(255,255,255))
            instruction2 = TextEntry((10, 25), instruction_text2, "default15", size = 15, color=(255,255,255))
            instruction3 = TextEntry((10, 45), instruction_text3, "default15", size = 15, color=(255,255,255))
            self.text = [instruction1, instruction2, instruction3]

        if self.veganBurger_meal_finished:
            instruction_text1 = "Your burger is ready to be served"
            instruction_text2 = "Pick up and bring to customer's plate."
            instruction1 = TextEntry((10, 5), instruction_text1, "default15", size = 15, color=(255,255,255))
            instruction2 = TextEntry((10, 25), instruction_text2, "default15", size = 15, color=(255,255,255))
            self.text = [instruction1, instruction2]
        
        if self.veganBurger_meal_served:
            instruction_text1 = "Now drag the customer's ticket"
            instruction_text2 = "over their meal to finish "
            instruction_text3 = "serving them."
            instruction1 = TextEntry((10, 5), instruction_text1, "default15", size = 15, color=(255,255,255))
            instruction2 = TextEntry((10, 25), instruction_text2, "default15", size = 15, color=(255,255,255))
            instruction3 = TextEntry((10, 45), instruction_text3, "default15", size = 15, color=(255,255,255))
            self.text = [instruction1, instruction2, instruction3]

        if self.veganBurger_ticket_dragged:
            instruction_text1 = "Great job! Now let's try it with more"
            instruction_text2 = "toppings and a drink. Click on "
            instruction_text3 = "the soda machine once a can is ready."
            instruction_text4 = "A new one is ready every 15 seconds."
            instruction1 = TextEntry((10, 5), instruction_text1, "default15", size = 15, color=(255,255,255))
            instruction2 = TextEntry((10, 25), instruction_text2, "default15", size = 15, color=(255,255,255))
            instruction3 = TextEntry((10, 45), instruction_text3, "default15", size = 15, color=(255,255,255))
            instruction4 = TextEntry((10, 65), instruction_text4, "default15", size = 15, color=(255,255,255))
            self.text = [instruction1, instruction2, instruction3, instruction4]

        if self.get_drink:
            instruction_text1 = "The soda is brought directly to the"
            instruction_text2 = "customer's plate."
            instruction1 = TextEntry((10, 5), instruction_text1, "default15", size = 15, color=(255,255,255))
            instruction2 = TextEntry((10, 25), instruction_text2, "default15", size = 15, color=(255,255,255))
            self.text = [instruction1, instruction2]

        if self.meatBurger_bun:
            instruction_text1 = "Now, pick up the burger bun"
            instruction_text2 = "and place on the prep station."
            instruction1 = TextEntry((10, 25), instruction_text1, "default15", size = 15, color=(255,255,255))
            instruction2 = TextEntry((10, 45), instruction_text2, "default15", size = 15, color=(255,255,255))
            self.text = [instruction1, instruction2]

        if self.meatBurger_bun_placed:
            instruction_text1 = "Great, now cook the patty on"
            instruction_text2 = "the grill."
            instruction1 = TextEntry((10, 25), instruction_text1, "default15", size = 15, color=(255,255,255))
            instruction2 = TextEntry((10, 45), instruction_text2, "default15", size = 15, color=(255,255,255))
            self.text = [instruction1, instruction2]

        if self.meatBurger_meat_cooking:
            instruction_text1 = "The toppings and meat (once cooked)" 
            instruction_text2 = "can be placed on the burger"
            instruction_text3 = "in any order."
            instruction1 = TextEntry((10, 5), instruction_text1, "default15", size = 15, color=(255,255,255))
            instruction2 = TextEntry((10, 25), instruction_text2, "default15", size = 15, color=(255,255,255))
            instruction3 = TextEntry((10, 45), instruction_text3, "default15", size = 15, color=(255,255,255))
            self.text = [instruction1, instruction2, instruction3]

        if self.meatBurger_meat_cooked:
            instruction_text1 = "The patty is cooked and ready to"
            instruction_text2 = "be placed in the burger. Ensure"
            instruction_text3 = "you include your toppings as well."
            instruction1 = TextEntry((10, 25), instruction_text1, "default15", size = 15, color=(255,255,255))
            instruction2 = TextEntry((10, 45), instruction_text2, "default15", size = 15, color=(255,255,255))
            instruction3 = TextEntry((10, 45), instruction_text3, "default15", size = 15, color=(255,255,255))
            self.text = [instruction1, instruction2, instruction3]

        if self.meatBurger_meat_burnt:
            instruction_text1 = "Oh no! Your patty burned!"
            instruction_text2 = "Throw away patty in trash"
            instruction_text3 = "and cook another."
            instruction1 = TextEntry((10, 5), instruction_text1, "default15", size = 15, color=(255,255,255))
            instruction2 = TextEntry((10, 25), instruction_text2, "default15", size = 15, color=(255,255,255))
            instruction3 = TextEntry((10, 45), instruction_text3, "default15", size = 15, color=(255,255,255))
            self.text = [instruction1, instruction2, instruction3]

        if self.meatBurger_meal_finished:
            instruction_text1 = "Now that the burger is completed,"
            instruction_text2 = "bring it to the customer."
            instruction1 = TextEntry((10, 5), instruction_text1, "default15", size = 15, color=(255,255,255))
            instruction2 = TextEntry((10, 25), instruction_text2, "default15", size = 15, color=(255,255,255))
            self.text = [instruction1, instruction2]
        
        if self.meatBurger_meal_served:
            instruction_text1 = "In order to complete this last order,"
            instruction_text2 = "drag the ticket over the meal."
            instruction1 = TextEntry((10, 5), instruction_text1, "default15", size = 15, color=(255,255,255))
            instruction2 = TextEntry((10, 25), instruction_text2, "default15", size = 15, color=(255,255,255))
            self.text = [instruction1, instruction2]

        # draw the instruction text
        for text in self.text:
            text.draw(drawSurface)
            
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
             
        

    def handle_foodlist_event(self, new_position):
        # for each item of food (and the trash can)
        for i in self.foodList:
            # can only click on them if they are a part of the current meal being made
            if self.tickets[0] is not None:
                if (i.item.stateType in self.tickets[0].ticketItems and not (i.item.stateType == 'bun' and 'hot dog meal' in self.tickets[0].ticketItems)) or ('hot dog meal' in self.tickets[0].ticketItems and i.item.stateType == 'hot dog bun') or ('hot dog meal' in self.tickets[0].ticketItems and i.item.stateType == 'hot dog meat') or ('cooked ' + i.item.stateType in self.tickets[0].ticketItems) or i.item.stateType == 'trash':
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
                            else:
                                # pick up item
                                self.trash.close_can()
                                self.chef.pickUp(i.item)
                                if i.item.stateType == 'hot dog bun':
                                    self.pickedUpBun = True
                                elif i.item.stateType == 'bun' and 'cooked vegan patty' in self.tickets[0].ticketItems:
                                    self.veganBurger_bun = True
                                elif i.item.stateType == 'bun' and 'cooked meat patty' in self.tickets[0].ticketItems:
                                    self.meatBurger_bun = True

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
                            if itemType == 'bun' and 'cooked vegan patty' in self.tickets[0].ticketItems:
                                self.veganBurger_bun_placed = True
                            elif itemType == 'bun' and 'cooked meat patty' in self.tickets[0].ticketItems:
                                self.meatBurger_bun_placed = True
                            elif itemType == 'cooked vegan patty':
                                self.meal_finished = True
                            elif (itemType == 'cooked meat patty' and ('lettuce' in x.burgerFSM.meal and 'cheese' in x.burgerFSM.meal)) or (itemType == 'cheese' and ('lettuce' in x.burgerFSM.meal and 'cooked meat patty' in x.burgerFSM.meal)) or (itemType == 'lettuce' and ('cooked meat patty' in x.burgerFSM.meal and 'cheese' in x.burgerFSM.meal)):
                                self.meatBurger_meal_finished = True
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
                            if itemType == 'hot dog bun':
                                self.placed_bun = True
                            if itemType == 'cooked hot dog meat':
                                self.meal_finished = True
                            x.hotdogMealFSM.updateHotDog(itemType)
                            index = self.mealPrepStations.index(x)
                            self.hotdog_images[index] = x.hotdogMealFSM.getStateImage((x.centroid[0]-35, x.centroid[1]-30))
                        # if holding an already made hot dog
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
                            if itemType == 'meat patty':
                                self.meatBurger_meat_cooking = True
                            y.pattyOn = True
                            self.timer = 0
                        # if chef is holding a hot dog, update the hot dog fsm
                        elif itemType == 'hot dog meat' and not (y.isHotDogOn() or y.isPattyOn()):
                            if y not in self.currently_cooking:
                                self.currently_cooking.append(y)
                            self.hotdog_image = y.hotdogFSM.getStateImage((y.centroid[0]-35, y.centroid[1]-10))
                            self.chef.dropOff()
                            self.cooking = True
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
                                if 'bun' in w.meal and 'cooked vegan patty' in w.meal:
                                    self.veganBurger_meal_served = True
                                if 'bun' in w.meal and 'cooked meat patty' in w.meal and 'lettuce' in w.meal and 'cheese' in w.meal:
                                    self.meatBurger_meal_served = True
                            elif itemType == 'hot dog meal':
                                item = self.chef.item
                                self.chef.dropOff()
                                self.meal_served = True
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
                                self.meatBurger_bun = True
                    # pick meal back up if chef isn't holding an item already, so that it can be moved to a different serving station or thrown in trash if needed
                    elif not self.chef.isHoldingItem() and self.meals[a] is not None:
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
                        ticket.dragging = True
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
                                    # check if meal and ticket items match and if customer name and ticket name match
                                    if sorted(serving_station.meal) == sorted(ticket.ticketItems) and serving_station.customer.name == ticket.name:
                                        # Fulfill the order by updating the meal FSM to the serve state
                                        serving_station.mealFSM.updateMeal(ticket)
                                        serving_station.mealFSM.reset()
                                        station_index = self.serving_stations.index(serving_station)
                                        self.meal_images[station_index] = serving_station.mealFSM.getStateImage(None, serving_station.mealFSM.position)
                                        serving_station.meal = serving_station.mealFSM.getMeal()
                                        self.ticket_dragged = True
                                        if 'hot dog meal' in ticket.ticketItems:
                                            self.meal1_done = True
                                        if 'cooked vegan patty' in ticket.ticketItems:
                                            self.veganBurger_ticket_dragged = True
                                            self.meal2_done = True
                                        if 'cooked meat patty' in ticket.ticketItems:
                                            self.meatBurger_ticket_dragged = True
                                            self.meal3_done = True
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
                        self.get_drink = True


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
        if self.score >= self.score_to_complete:
            return True
        else:
            return False
        
    def getScore(self):
        return str(self.score)

    def update(self, seconds):
        # check if game over
        if len(self.customers_done) >= self.customers_to_serve:
            self.gameOver = True
        # update all the timers
        self.gameTime += seconds
        self.cola_machine.time += seconds  
        # get the customer queue      
        self.customer_queue = self.customerManager.get_queue()
        self.customers_done = self.customerManager.get_customers_done()
        # send first customer in
        if self.gameTime >= 1 and not self.completed_tickets[0]:
            self.meal1_done = True
            self.completed_tickets[0] = True
        
        #for x in self.customer_queue:
        #    if x is not None:
        #        x.decreasePatience(seconds)
        #        x.update(seconds)

        for y in self.mealPrepStations:
            if 'bun' in y.burgerFSM.meal and 'cooked vegan patty' in y.burgerFSM.meal:
                self.veganBurger_meal_finished = True

        # update chef sprite
        self.chef.update(seconds)
        Drawable.updateOffset(self.chef, self.size)
        if self.chef.isHoldingItem() and (self.chef.item.getStateType() == 'cooked meat patty' or self.chef.item.getStateType() == 'cooked meat patty'):
            self.patty_image = None
        
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
        
        # update customers
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
            self.done_cooking = True
            if 'cooked vegan patty' in self.tickets[0].ticketItems:
                self.veganBurger_meat_cooked = True
            if 'cooked meat patty' in self.tickets[0].ticketItems:
                self.meatBurger_meat_cooked = True
        elif percentage > 1.5:
            # draw a red circle since it is burnt
            pygame.draw.circle(drawSurface, (255, 0, 0), position, radius)
            self.burnt = True
            if 'cooked vegan patty' in self.tickets[0].ticketItems:
                self.veganBurger_meat_burnt = True
            if 'cooked meat patty' in self.tickets[0].ticketItems:
                self.meatBurger_meat_burnt = True


    def draw_arc(self, drawSurface, position, radius, percentage, color):
        # draw the arc for the percentage left
        angle = 360 * percentage
        pygame.draw.arc(drawSurface, color, (position[0] - radius, position[1] - radius, 2 * radius, 2 * radius), math.radians(-90), math.radians(-90 + angle), width=6)


    def spawn_customer(self, new_customer=None):
        # spawn customer based on a predetermined order for the tutorial
        index = 0
        if len(self.customers_done) == 0:
            index = 0
        elif len(self.customers_done) == 1:
            index = 1
        elif len(self.customers_done) == 2:
            index = 2
        if new_customer is None:
            new_customer = self.customerManager.add_person()
        else:
            new_customer = new_customer
        if self.tickets[0] == None:
            if index == 0:
                new_customer.order.generatePreDeterminedOrder(self.ticket_position1, 'hot dog')
            elif index == 1:
                new_customer.order.generatePreDeterminedOrder(self.ticket_position1, 'burger', ['cooked vegan patty'])
            elif  index == 2:
                new_customer.order.generatePreDeterminedOrder(self.ticket_position1, 'burger', ['cooked meat patty', 'lettuce', 'cheese'])
            self.tickets[0] = new_customer.order
            self.customers[0] = new_customer
        self.spawned = True
        return new_customer
    

    def is_time_to_spawn_customer(self):
        # spawn customer based on whether the last meal is already done
        if self.meal1_done:
            # turn to false so it doesn't repeat
            self.meal1_done = False
            return True
        if self.meal2_done:
            self.meal2_done = False
            return True
        if self.meal3_done:
            self.meal3_done = False
            return True


    def fulfill_order(self, order):
        # Called when the player fulfills an order
        self.last_order_fulfilled_time = self.gameTime
        index = self.tickets.index(order)
        self.tickets[index] = None
        self.customer_queue[index].order = None
        self.customer_queue[index].order.filled = True
        # if ticket is dragged to the order, then order is fulfilled
