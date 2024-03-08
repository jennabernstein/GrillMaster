import random

class Ticket:
    def __init__(self):
        self.ticket = ['bun']
        self.level = 1

    def generateOrder(self):
        meat = random.randint(0,1)
        if meat ==1:
            self.ticket.append('real meat patty')
        else:
            self.ticket.append('vegan patty')
        
        toppings = random.randint(0,2)
        type = random.randint(0,2)
        if toppings == 1 or toppings == 2:
            type = random.randint(0,2)
            if type == 0:
                self.ticket.append('lettuce')
                if toppings == 2:
                    type = random.randint(0,1)
                    if type == 0:
                        self.ticket.append('tomato')
                    else:
                        self.ticket.append('cheese')
            elif type == 1:
                self.ticket.append('tomato')
                if toppings == 2:
                    type = random.randint(0,1)
                    if type == 0:
                        self.ticket.append('lettuce')
                    else:
                        self.ticket.append('cheese')
            else:
                self.ticket.append('cheese')
                if toppings == 2:
                    type = random.randint(0,1)
                    if type == 0:
                        self.ticket.append('tomato')
                    else:
                        self.ticket.append('lettuce')

    def generateTicketImage(self):
        pass

    def getTicket(self):
        return self.ticket

    def highlightTicket(self):
        pass

    def finishTicket(self):
        pass

ticket = Ticket()
ticket.generateOrder()
print(ticket.getTicket())