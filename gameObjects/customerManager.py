import random
from . import Customer
from FSMs import WalkingFSM

class CustomerManager():
    def __init__(self, level):
        self.level = level
        self.queue = [None, None, None]
        self.nextCustomers = []
        self.timer = 0
        self.usedName = []
        self.names = ["Eva", "Ana", "Mia", "Ella", "Sofia", "Claire", "Liam", "Jake", "Clay", "Pete", "Sean", "Sam",
                      "Leo", "Noah", "Liam", "Oli", "Jay", "Jack", "Ben", "Eli", "Will", "Alex", "Lucas", "Will"]
        self.stations = [None, None, None]
        self.customers_done = []
        self.level1spawn = False

    def get_queue(self):
        return self.queue
    
    def get_person(self):
        for i in self.queue:
            if i is not None:
                return i
            
    def remove_person(self, person):
        if person in self.queue:
            index = self.queue.index(person)
            self.queue[index] = None
            self.stations[index].customer = None
    
    def add_person(self):
        customer = Customer(self.generateName())
        customer.start_time = self.timer
        customer.patience = customer.start_time + customer.patience
        for i in self.stations:
            if i.customer is None:
                customer.setStation(i)
                i.customer = customer
                break
        for i in range(len(self.queue)):
            if self.queue[i] is None:
                self.queue[i] = customer
                break
        return customer
    
    def update_timer(self, seconds):
        self.timer += seconds

    def get_customers_done(self):
        return self.customers_done

    def update_queue(self, seconds):
        for i in self.queue:
            if i is not None:
                if i.needToMove():
                    i.update(seconds)
                if i.isSatisfied() or i.is_unpatient():
                    self.customers_done.append(i)
                    self.remove_person(i)
                    self.level1spawn = True
                    

    def generateName(self):
        name = random.choice(self.names)
        self.names.remove(name)
        return name