from . import Mobile, Drawable
from FSMs import CustomerWalkingFSM
import random
from .ticket import Ticket
import numpy as np


class Customer(Drawable):   
    def __init__(self, name):
        if name in ["Eva", "Ana", "Mia", "Ella", "Sofia", "Claire"]:
            image = "customer3.png"
        elif name in ["Liam", "Jake", "Clay", "Pete", "Sean", "Sam"]:
            image = "customer4.png"
        elif name in ["Leo", "Noah", "Liam", "Oli", "Jay", "Jack"]:
            image = "customer1.png"
        elif name in ["Ben", "Eli", "Will", "Alex", "Lucas", "Will"]:
            image = "customer2.png"
        super().__init__((500, 500), image, offset=(0,0), scale=1)
        self.patience = 40  # Initial patience level (adjust as needed)
        self.preferred_dish = None
        self.order = Ticket(name)
        self.current_patience = 0
        self.speed = 100
        self.name = name
        self.station = None
        self.framesPerSecond = 12
        self.nFrames = 8
        self.nFramesList = {"standing" : 1, "moving" : 3}
        self.rowList = { "standing" : 1, "moving" : 2}
        self.framesPerSecondList = {"standing" : 8, "moving" : 8}
        #self.FSManimated = CustomerWalkingFSM(self)
        self.target_position = None
        self.start_time = 0
        self.timer_position = self.position[0] + 125, self.position[1] + 150

        self.timer = None

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
    
    def getScore(self):
        if self.is_unpatient():
            score = 0
        elif self.get_patience_percentage() >= .75:
            score = 300
        elif self.get_patience_percentage() >= .5:
            score = 200
        elif self.get_patience_percentage() >= .25:
            score = 100
        else:
            score = 75
        score += int(self.get_patience_percentage() * 100)
        print(self.get_patience_percentage())
        return score
    
    def is_unpatient(self):
        if self.current_patience == self.patience:
            return True
        
    def get_patience_percentage(self):
        return self.current_patience / self.patience

    def generateCustomerImage(self, row):
        self.row = row

    def setName(self, name):
        self.name = name

    def setStation(self, station):
        self.station = station
        if station is not None:
            self.target_position = station.customerPosition
            self.position = self.target_position
            self.timer_position = self.position[0] + 100, self.position[1] + 100
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

