from . import Mobile
from FSMs import WalkingFSM, AccelerationFSM
from utils import vec, RESOLUTION
from shapely.geometry import Polygon, Point

from pygame.locals import *

import pygame
import numpy as np


class Chef(Mobile):
   def __init__(self, position, scale=5):
      super().__init__(position, "chef sprite.png", scale)
      # Animation variables specific to Kirby
      self.framesPerSecond = 12
      self.nFrames = 8
      
      self.nFramesList = {
         "standing" : 1,
         "moving" : 8,
         "forward"   : 7,
         "quarterForward" : 7,
         "side" : 7,
         "back" : 7,
         "quarterBack" : 7
      }

      self.rowList = {
         "standing" : 0,
         "moving" : 0,
         "forward"   : 0,
         "quarterForward" : 1,
         "side" : 2,
         "back" : 3,
         "quarterBack" : 4
      }
      
      self.framesPerSecondList = {
         "standing" : 2,
         "moving" : 8,
         "forward"   : 8,
         "quarterForward" : 8,
         "side" : 2,
         "back" : 2,
         "quarterBack" : 2
      }
            
      self.FSManimated = WalkingFSM(self)
      self.LR = AccelerationFSM(self, axis=0)
      self.UD = AccelerationFSM(self, axis=1)
      self.size = self.getSize()
      self.allowed_polygon = Polygon([(10, 350), (10, 250), (450, 40), (450, 90), (950, 300), (950, 700), (600, 700)])
      self.rect = pygame.Rect(self.position[0], self.position[1]+40, self.image.get_width(), self.image.get_height()-60)
      self.position = np.array(position, dtype=int)
      self.position = self.position[0], self.position[1]+40
      self.target_position = None
      self.speed = 5


   def is_position_valid(self, new_position):
    # Convert the new position to a Point object
    point = Point(new_position[0], new_position[1] + 40)

    # Check if the Point is within the allowed polygon
    if not point.within(self.allowed_polygon):
        return False

    # Check if the new position + velocity is within the allowed boundaries
    future_position = Point(point.x + self.velocity[0], point.y + self.velocity[1])

    if not future_position.within(self.allowed_polygon):
        return False

    return True

   def handleEvent(self, event):
       return super().handleEvent(event)

   def move(self, target_position):
      self.target_position = tuple(target_position)
        

   def updateOffset(self, size):
        # Calculate the offset based on the width of the first sprite
        first_sprite_width = self.FSManimated.spriteManager.getSize(self.imageName)[0]
        self.offset = (size.x - first_sprite_width, size.y)
   
   def update(self, seconds): 
      if self.target_position:
         direction = np.array(self.target_position) - self.position
         distance = np.linalg.norm(direction)

         if distance > self.speed:
            normalized_direction = direction / distance
            self.position = tuple(np.array(self.position) + (normalized_direction * self.speed).astype(int))
         else:
            self.position = np.array(self.target_position, dtype=int)
            self.target_position = None

      super().update(seconds)

   
  