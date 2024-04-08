import random
from . import Drawable, TextEntry
import pygame

class Ticket(Drawable):
    def __init__(self, name):
        super().__init__()
        self.ticketItems = ['bun']
        self.level = 1
        self.ticket = Drawable()
        self.image = Drawable()
        self.filled = False
        self.dragging = False
        self.cola = Drawable()
        self.name = name
        self.customerName = TextEntry((0,0), '')

    def generatePreDeterminedOrder(self, position, HDorB, items=[]):
        if HDorB == 'hot dog':
            self.ticketItems.append('hot dog meal')
            ticketImage = Drawable(position, "tickets/ticket - hot dog.png", scale = 0.31)
        
        elif HDorB == 'burger':
            if 'cooked meat patty' in items:
                self.ticketItems.append('cooked meat patty')
                ticketImage = Drawable(position, "tickets/ticket - meat patty.png", scale=0.3)
                if 'lettuce' in items and 'cheese' in items:
                    self.ticketItems.append('lettuce')
                    self.ticketItems.append('cheese')
                    ticketImage = Drawable(position, "tickets/ticket - meat patty, lettuce, cheese.png", scale=0.3)
                self.ticketItems.append('cola')
            elif 'cooked vegan patty' in items:
                self.ticketItems.append('cooked vegan patty')
                ticketImage = Drawable(position, "tickets/ticket - vegan patty.png", scale=0.3)

        self.cola = Drawable((ticketImage.position[0]+45,ticketImage.position[1]-10), "food/cola.png", None, 2)
        print(self.name)
        self.customerName = TextEntry((ticketImage.position[0]+10,ticketImage.position[1]+25), self.name, "default10")
        print(self.customerName.position)
        self.image = ticketImage
        print(self.name)
            

    def generateOrder(self, position):
        drink = random.choice(['True', 'False'])
        HDorB = random.choice(['hot dog', 'burger', 'burger'])
        if HDorB == 'burger':
            meat = random.randint(0,1)
            if meat == 1:
                self.ticketItems.append('cooked meat patty')
                ticketImage = Drawable(position, "tickets/ticket - meat patty.png", scale=0.3)
                toppings = random.randint(0,2)
                if toppings == 3:
                    self.ticketItems.append('lettuce')
                    self.ticketItems.append('cheese')
                    self.ticketItems.append('tomato')
                    ticketImage = Drawable(position, "tickets/ticket - meat patty, tomato, lettuce, cheese.png", scale=0.3)
                elif toppings == 1 or toppings == 2:
                    type = random.choice(['lettuce', 'tomato', 'cheese'])
                    if type == 'lettuce':
                        self.ticketItems.append('lettuce')
                        ticketImage = Drawable(position, "tickets/ticket - meat patty, lettuce.png", scale=0.3)
                        if toppings == 2:
                            type = random.choice(['tomato', 'cheese'])
                            if type == 'tomato':
                                self.ticketItems.append('tomato')
                                ticketImage = Drawable(position, "tickets/ticket - meat patty, tomato, lettuce.png", scale=0.3)
                            else:
                                self.ticketItems.append('cheese')
                                ticketImage = Drawable(position, "tickets/ticket - meat patty, lettuce, cheese.png", scale=0.3)
                    elif type == 'tomato':
                        self.ticketItems.append('tomato')
                        ticketImage = Drawable(position, "tickets/ticket - meat patty, tomato.png", scale=0.3)
                        if toppings == 2:
                            type = random.choice(['lettuce', 'cheese'])
                            if type == 'lettuce':
                                self.ticketItems.append('lettuce')
                                ticketImage = Drawable(position, "tickets/ticket - meat patty, tomato, lettuce.png", scale=0.3)
                            else:
                                self.ticketItems.append('cheese')
                                ticketImage = Drawable(position, "tickets/ticket - meat patty, tomato, cheese.png", scale=0.3)
                    else:
                        self.ticketItems.append('cheese')
                        ticketImage = Drawable(position, "tickets/ticket - meat patty, cheese.png", scale=0.3)
                        if toppings == 2:
                            type = random.choice(['tomato', 'lettuce'])
                            if type == 'tomato':
                                self.ticketItems.append('tomato')
                                ticketImage = Drawable(position, "tickets/ticket - meat patty, tomato, cheese.png", scale=0.3)
                            else:
                                self.ticketItems.append('lettuce')
                                ticketImage = Drawable(position, "tickets/ticket - meat patty, lettuce, cheese.png", scale=0.3)
            else:
                self.ticketItems.append('cooked vegan patty')
                ticketImage = Drawable(position, "tickets/ticket - vegan patty.png", scale=0.3)
                toppings = random.randint(0,3)
                if toppings == 3:
                    self.ticketItems.append('lettuce')
                    self.ticketItems.append('cheese')
                    self.ticketItems.append('tomato')
                    ticketImage = Drawable(position, "tickets/ticket - vegan patty, tomato, lettuce, cheese.png", scale=0.3)
                elif toppings == 1 or toppings == 2:
                    type = random.choice(['lettuce', 'tomato', 'cheese'])
                    if type == 'lettuce':
                        self.ticketItems.append('lettuce')
                        ticketImage = Drawable(position, "tickets/ticket - vegan patty, lettuce.png", scale=0.3)
                        if toppings == 2:
                            type = random.choice(['tomato', 'cheese'])
                            if type == 'tomato':
                                self.ticketItems.append('tomato')
                                ticketImage = Drawable(position, "tickets/ticket - vegan patty, tomato, lettuce.png", scale=0.3)
                            else:
                                self.ticketItems.append('cheese')
                                ticketImage = Drawable(position, "tickets/ticket - vegan patty, lettuce, cheese.png", scale=0.3)
                    elif type == 'tomato':
                        self.ticketItems.append('tomato')
                        ticketImage = Drawable(position, "tickets/ticket - vegan patty, tomato.png", scale=0.3)
                        if toppings == 2:
                            type = random.choice(['lettuce', 'cheese'])
                            if type == 'lettuce':
                                self.ticketItems.append('lettuce')
                                ticketImage = Drawable(position, "tickets/ticket - vegan patty, tomato, lettuce.png", scale=0.3)
                            else:
                                self.ticketItems.append('cheese')
                                ticketImage = Drawable(position, "tickets/ticket - vegan patty, tomato, cheese.png", scale=0.3)
                    else:
                        self.ticketItems.append('cheese')
                        ticketImage = Drawable(position, "tickets/ticket - vegan patty, cheese.png", scale=0.3)
                        if toppings == 2:
                            type = random.choice(['tomato', 'lettuce'])
                            if type == 'tomato':
                                self.ticketItems.append('tomato')
                                ticketImage = Drawable(position, "tickets/ticket - vegan patty, tomato, cheese.png", scale=0.3)
                            else:
                                self.ticketItems.append('lettuce')
                                ticketImage = Drawable(position, "tickets/ticket - vegan patty, lettuce, cheese.png", scale=0.3)
        elif HDorB == 'hot dog':
            self.ticketItems.append('hot dog meal')
            ticketImage = Drawable(position, "tickets/ticket - hot dog.png", scale = 0.31)
        if drink == 'True':
            self.ticketItems.append('cola')
        self.cola = Drawable((ticketImage.position[0]+45,ticketImage.position[1]-10), "food/cola.png", None, 2)
        self.customerName = TextEntry((ticketImage.position[0]+10,ticketImage.position[1]+25), self.name, "default10")
        self.image = ticketImage

    def updateRectPosition(self, position):
        new_x = position[0]  # New x-coordinate
        new_y = position[1]  # New y-coordinate
        self.image.rect.left = new_x
        self.image.rect.top = new_y

    def getTicket(self):
        return self.ticket

    def setPosition(self, new_position):
        self.position = new_position

    def finishTicket(self):
        self.filled = True

    def isFulfilled(self):
        if self.filled:
            return True
        
    def getStateType(self):
        return "ticket"
