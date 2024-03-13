from . import Mobile
from FSMs import WalkingFSM
from utils import vec, RESOLUTION
from shapely.geometry import Polygon, Point

from pygame.locals import *

import pygame
import numpy as np
from . import Drawable


class Chef(Mobile):
   def __init__(self, position, scale=5):
      super().__init__(position, "chef sprite.png", scale)
      # Animation variables specific to Kirby
      self.framesPerSecond = 12
      self.nFrames = 1
      
      self.nFramesList = {
         "standing" : 1,
         "moving" : 8,
         "forward"   : 8,
         "back" : 8,
         "standingforward" : 1,
         "standingback": 1
      }

      self.rowList = {
         "standing" : 1,
         "moving" : 1,
         "forward"   : 2,
         "back" : 3,
         "standingforward" : 4,
         "standingback": 5
      }
      
      self.framesPerSecondList = {
         "standing" : 8,
         "moving" : 8,
         "forward"   : 8,
         "back" : 8,
         "standingforward" : 1,
         "standingback": 1
      }

      self.FSManimated = WalkingFSM(self)
      self.size = self.getSize()
      self.rect = pygame.Rect(self.position[0], self.position[1], self.image.get_width(), self.image.get_height())
      self.position = np.array(position, dtype=int)
      self.position = self.position[0], self.position[1]
      self.target_position = None
      self.speed = 200
      self.holdingItem = False
      self.itemOffset = vec(70,130)
      self.item = Drawable()

   def handleEvent(self, event):
      return super().handleEvent(event)

   def move(self, target_position):
      self.target_position = tuple(target_position)
         
   def pickUp(self, item):
         if not self.holdingItem:
            self.item = item
         self.holdingItem = True

   def dropOff(self):
         self.holdingItem = False
         self.item = Drawable()

   def updateOffset(self, size):
      first_sprite_width = self.FSManimated.spriteManager.getSize(self.imageName)[0]
      scaled_size = vec(*self.image.get_size())
      self.offset = (scaled_size.x - first_sprite_width, scaled_size.y)

   def isHoldingItem(self):
      return self.holdingItem
   
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

         if self.holdingItem:
            self.item.position = self.itemOffset + self.position
      

      self.FSManimated.updateState()
      self.FSManimated.updateMovement(seconds)
