from . import Mobile, Drawable
from FSMs import CustomerWalkingFSM
import random
from .ticket import Ticket
import numpy as np


class Customer(Drawable):   
    def __init__(self, name):
        if name in ['Alice']:
            image = "customer1.png"
        elif name in ['Eva']:
            image = "customer2.png"
        elif name in ['Bob', 'Charlie', 'Chad']:
            image = "customer3.png"
        elif name in ['David', 'Frank']:
            image = "customer4.png"
        super().__init__((500, 500), image, offset=(0,0), scale=1)
        self.patience = 40  # Initial patience level (adjust as needed)
        self.preferred_dish = None
        self.order = Ticket()
        self.current_patience = 0
        self.speed = 100
        self.name = ''
        self.station = None
        self.framesPerSecond = 12
        self.nFrames = 8
        self.nFramesList = {"standing" : 1, "moving" : 3}
        self.rowList = { "standing" : 1, "moving" : 2}
        self.framesPerSecondList = {"standing" : 8, "moving" : 8}
        #self.FSManimated = CustomerWalkingFSM(self)
        self.target_position = None
        self.start_time = 0

    def needToMove(self):
        if self.target_position is not None:
            return tuple(self.target_position) != tuple(self.position)
        else:
            return False
    
    def decreasePatience(self, seconds):
        # Decrease the customer's patience by the specified amount
        self.current_patience += seconds
        if self.current_patience > self.patience:
            self.current_patience = self.patience

    def isSatisfied(self):
        # Check if the customer is satisfied based on the order fulfillment
        # You can compare the order with the player's prepared dishes
        return self.order.isFulfilled()
    
    def is_unpatient(self):
        if self.current_patience == self.patience:
            return True

    def generateCustomerImage(self, row):
        self.row = row

    def setName(self, name):
        self.name = name

    def setStation(self, station):
        self.station = station
        if station is not None:
            self.target_position = station.customerPosition
            self.position = self.target_position
            #self.FSManimated.move()
        else:
            self.target_position = None
            #self.FSManimated.stop()


    def update(self, seconds): 
        super().update(seconds)
        if self.target_position:
            direction = np.array(self.target_position) - self.position
            distance = np.linalg.norm(direction)
            if distance > 5:
                normalized_direction = direction / distance
                self.velocity = normalized_direction * self.speed
            else:
                self.position = np.array(self.target_position, dtype=int)
                self.target_position = None
                self.velocity = np.array([0, 0], dtype=int)
        #print(self.FSManimated.current_state)
        #self.FSManimated.updateState()
        #self.FSManimated.updateMovement(seconds)
