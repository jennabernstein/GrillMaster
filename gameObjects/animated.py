from . import Drawable
from utils import SpriteManager
import pygame
import numpy as np

class Animated(Drawable):
    
    def __init__(self, position=(0,0), fileName="", scale=1):
        super().__init__(position, fileName, (0,0), scale)
        self.fileName = fileName
        self.row = 0
        self.frame = 0
        self.nFrames = 1
        self.nFramesList = []
        self.animate = True
        self.framesPerSecond = 8
        self.animationTimer = 0
        self.FSManimated = None
        self.scale = scale
    
    def update(self, seconds, target_position=None):
        if self.FSManimated:
            self.FSManimated.updateState()
            
        if not self.animate:
            return
        
        self.animationTimer += seconds 
        self.nFrames = self.nFramesList.get(str(self.FSManimated.current_state.id), 1)
        # print('velocity: ' , self.velocity, 'frame: ' ,self.frame, 'state: ' , self.FSManimated.current_state.id)

        
        if self.animationTimer > 1 / self.framesPerSecond:
            self.frame += 1
            self.frame %= self.nFrames
            self.animationTimer -= 1 / self.framesPerSecond
            self.image = SpriteManager.getInstance().getSprite(self.fileName, (self.frame, self.row))
            self.image = pygame.transform.scale(self.image, (self.image.get_size()[0]*self.scale, self.image.get_size()[1]*self.scale))

        if target_position is not None:
            direction = np.array(target_position) - np.array(self.position)
            distance = np.linalg.norm(direction)

            if distance > self.speed:
                normalized_direction = direction / distance
                self.position = tuple(np.array(self.position) + (normalized_direction * self.speed).astype(int))
            else:
                self.position = np.array(target_position, dtype=int)
                # Reset target_position to None
                target_position = None
