from . import Drawable
import random
from .ticket import Ticket


class Customer(Drawable):   
    def __init__(self):
        self.patience = 30  # Initial patience level (adjust as needed)
        self.preferred_dish = None
        self.order = Ticket()

    def generateCustomerName(self):
        names = ['Alice', 'Bob', 'Charlie', 'David', 'Eva', 'Frank']
        self.name = random.choice(names)

    
    def decreasePatience(self):
        # Decrease the customer's patience by the specified amount
        self.patience -= 1
        if self.patience < 0:
            self.patience = 0

    def isSatisfied(self):
        # Check if the customer is satisfied based on the order fulfillment
        # You can compare the order with the player's prepared dishes
        return self.order.isFulfilled()  # Example: Check if the order is fulfilled

    def generateCustomerImage(self):
        pass