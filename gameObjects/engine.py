import pygame

from . import Drawable
from .chef import Chef
from .patties import Patties
from .trash import Trash
from .tomatoes import Tomatoes
from .lettucePlate import Lettuces
from .cheesePlate import Cheeses
from .onions import Onions

from utils import vec, RESOLUTION

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
        self.tomatoes = Tomatoes((200, 200))
        self.onions = Onions((250, 175))
        self.lettuces = Lettuces((290, 150))
        self.cheeses = Cheeses((330, 120))
        self.pinkPrep = self.scaleDrawable(self.pinkPrep, (325, 300))
        self.pinkCounter = self.scaleDrawable(self.pinkCounter, (300, 250))
        self.longPinkCounter = self.scaleDrawable(self.longPinkCounter,(640, 375))
        self.customerCounter = self.scaleDrawable(self.customerCounter, (700, 420))
        self.foodList = [self.patties1, self.patties2, self.trash, self.tomatoes, self.onions, self.lettuces, self.cheeses]
        
        

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
        self.patties1.draw(drawSurface)
        self.patties2.draw(drawSurface)
        self.tomatoes.draw(drawSurface)
        self.cheeses.draw(drawSurface)
        self.onions.draw(drawSurface)
        self.lettuces.draw(drawSurface)
        self.chef.draw(drawSurface)
        if self.chef.isHoldingItem():
            self.chef.item.draw(drawSurface)
        self.pinkPrep.draw(drawSurface)
        self.customerCounter.draw(drawSurface)
        
        
        
            
    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            new_position = event.pos
            for i in self.foodList:
                if i.collide(new_position):
                    self.chef.move((i.position[0] + i.chefPos[0], i.position[1] + i.chefPos[1]))
                    if i == self.trash:
                        self.trash.open_can()
                        self.chef.dropOff()
                    else:
                        print(self.chef.item, self.chef.item.position)
                        self.chef.pickUp(i.item)


        self.trash.close_can()
    
    def update(self, seconds):
        self.chef.update(seconds)
        Drawable.updateOffset(self.chef, self.size)
