import pygame

from . import Drawable
from .chef import Chef
from .patties import Patties
from .trash import Trash

from utils import vec, RESOLUTION

class GameEngine(object):
    import pygame

    def __init__(self):       
        self.chef = Chef((500,500))
        self.size = vec(*RESOLUTION)
        self.background = Drawable((0,0), "kitchen background.png")
        self.pinkCounter = Drawable((500,150), "pink counter.png")
        self.pinkPrep = Drawable((0, 425), "pink prep.png")
        self.longPinkCounter = Drawable((-120, 70), "pink long counter.png")
        self.trash = Trash((455, 100), (0,0))
        self.patties1 = Patties((180, 150), (0,0))
        self.patties2 = Patties((100, 200), (1, 0))
        self.pinkPrep = self.scaleDrawable(self.pinkPrep, (325, 300))
        self.pinkCounter = self.scaleDrawable(self.pinkCounter, (300, 250))
        self.longPinkCounter = self.scaleDrawable(self.longPinkCounter,(640, 375))
        self.foodList = [self.patties1, self.patties2, self.trash]
        

    def scaleDrawable(self, drawable, new_size):
        # Use pygame.transform.scale to scale the image
        scaled_image = pygame.transform.scale(drawable.image, new_size)

        # Create a new Drawable with the scaled image
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
        #pygame.draw.polygon(drawSurface, [255, 255, 255], ([(10, 350), (10, 300), (480, 90), (950, 300), (950, 700), (600, 700)]))
        #pygame.draw.rect(drawSurface, [0,0,0], self.chef.rect)
        self.chef.draw(drawSurface)
        self.pinkPrep.draw(drawSurface)
        
        
        
            
    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            new_position = event.pos
            for i in self.foodList:
                if i.collide(new_position):
                    self.chef.move(i.chefPos)
    
    def update(self, seconds):
        self.chef.update(seconds)
        Drawable.updateOffset(self.chef, self.size)
