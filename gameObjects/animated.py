from . import Drawable
from utils import SpriteManager
import pygame

class Animated(Drawable):
    
    def __init__(self, position=(0,0), fileName="", scale=1):
        super().__init__(position, fileName, (0,0), scale)
        self.fileName = fileName
        self.row = 0
        self.frame = 0
        self.nFrames = 1
        self.animate = True
        self.framesPerSecond = 8
        self.animationTimer = 0
        self.FSManimated = None
        self.scale = scale
        self.direction = "down"  # Default direction

    def update(self, seconds):
        if self.FSManimated:
            self.FSManimated.updateState()
            
        if not self.animate:
            return
        
        self.animationTimer += seconds 
           
        if self.animationTimer > 1 / self.framesPerSecond:
            self.frame += 1
            self.frame %= self.nFrames
            self.animationTimer -= 1 / self.framesPerSecond

            

            self.image = SpriteManager.getInstance().getSprite(self.fileName,
                                        (self.frame, self.row))
            self.image = pygame.transform.scale(self.image, (self.image.get_size()[0]*self.scale, self.image.get_size()[1]*self.scale))
