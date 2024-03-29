import random
from . import Drawable
import pygame

class Ticket(Drawable):
    def __init__(self):
        super().__init__()
        self.ticketItems = ['bun']
        self.level = 1
        self.ticket = Drawable()
        self.image = Drawable()
        self.filled = False
        self.dragging = False

    def generateOrder(self, position):
        HDorB = random.choice(['hot dog', 'burger', 'burger'])
        if HDorB == 'burger':
            meat = random.randint(0,1)
            if meat == 1:
                self.ticketItems.append('cooked meat patty')
                ticketImage = Drawable(position, "tickets/ticket - meat patty.png", scale=0.3)
                toppings = random.randint(0,2)
                if toppings == 3:
                    self.ticketItems.append('lettuce', 'cheese', 'tomato')
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
                            if type == 0:
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
                            if type == 0:
                                self.ticketItems.append('tomato')
                                ticketImage = Drawable(position, "tickets/ticket - meat patty, tomato, cheese.png", scale=0.3)
                            else:
                                self.ticketItems.append('lettuce')
                                ticketImage = Drawable(position, "tickets/ticket - meat patty, lettuce, cheese.png", scale=0.3)
            else:
                self.ticketItems.append('cooked vegan patty')
                ticketImage = Drawable(position, "tickets/ticket - vegan patty.png", scale=0.3)
                toppings = random.randint(0,2)
                if toppings == 3:
                    self.ticketItems.append('lettuce', 'cheese', 'tomato')
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
                            if type == 0:
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
                            if type == 0:
                                self.ticketItems.append('tomato')
                                ticketImage = Drawable(position, "tickets/ticket - vegan patty, tomato, cheese.png", scale=0.3)
                            else:
                                self.ticketItems.append('lettuce')
                                ticketImage = Drawable(position, "tickets/ticket - vegan patty, lettuce, cheese.png", scale=0.3)
        elif HDorB == 'hot dog':
            self.ticketItems.append('hot dog meal')
            ticketImage = Drawable(position, "tickets/ticket - hot dog.png", scale = 0.31)
        self.image = ticketImage


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
