from . import Drawable
from utils import SpriteManager
import pygame
import numpy as np

class Animated(Drawable):
    
    def __init__(self, position=(0, 0), fileName="", scale=1):
        super().__init__(position, fileName, (0, 0), scale)
        self.fileName = fileName
        self.row = 0
        self.frame = 0
        self.nFrames = 1
        self.nFramesList = {}
        self.animate = True
        self.framesPerSecond = 8
        self.animationTimer = 0
        self.FSManimated = None
        self.scale = scale

        # Load the original image at the larger scale
        original_image = SpriteManager.getInstance().getSprite(self.fileName, (0, self.row))
        original_image = pygame.transform.scale(original_image, (original_image.get_size()[0] * self.scale, original_image.get_size()[1] * self.scale))
        self.original_image = original_image
        self.image = self.original_image
    
    def update(self, seconds, target_position=None):
        if self.FSManimated:
            self.FSManimated.updateState()

        # Handle animation
        if self.animate:
            self.animationTimer += seconds 
            self.nFrames = self.nFramesList.get(str(self.FSManimated.current_state.id), 1)

            
            if self.animationTimer > 1 / self.framesPerSecond:
                self.frame += 1
                self.frame %= self.nFrames
                self.animationTimer -= 1 / self.framesPerSecond
                
            animated_image = SpriteManager.getInstance().getSprite(self.fileName, (self.frame, self.row))
            animated_image = pygame.transform.scale(animated_image, (animated_image.get_size()[0] * self.scale, animated_image.get_size()[1] * self.scale))
            self.image = animated_image

        # Handle movement
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
