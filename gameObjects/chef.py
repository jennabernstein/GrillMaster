from . import Mobile
from FSMs import WalkingFSM, AccelerationFSM
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
         #"forward"   : 7,
         #"quarterForward" : 7,
         #"side" : 7,
         #"back" : 7,
         #"quarterBack" : 7
      }

      self.rowList = {
         "standing" : 0,
         "moving" : 0,
         #"forward"   : 0,
         #"quarterForward" : 1,
         #"side" : 2,
         #"back" : 3,
         #"quarterBack" : 4
      }
      
      self.framesPerSecondList = {
         "standing" : 1,
         "moving" : 8,
         #"forward"   : 8,
         #"quarterForward" : 8,
         #"side" : 2,
         #"back" : 2,
         #"quarterBack" : 2
      }
            
      self.FSManimated = WalkingFSM(self)
      self.size = self.getSize()
      self.allowed_polygon = Polygon([(10, 350), (10, 250), (450, 40), (450, 90), (950, 300), (950, 700), (600, 700)])
      self.rect = pygame.Rect(self.position[0], self.position[1]+40, self.image.get_width(), self.image.get_height()-60)
      self.position = np.array(position, dtype=int)
      self.position = self.position[0], self.position[1]+40
      self.target_position = None
      self.speed = 150
      self.holdingItem = False
      self.itemOffset = vec(70,150)
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
        if self.FSManimated.current_state == self.FSManimated.moving:
            self.FSManimated.stop()
        self.holdingItem = False
        self.item = Drawable()
        

   def updateOffset(self, size):
        # Calculate the offset based on the width of the first sprite
        first_sprite_width = self.FSManimated.spriteManager.getSize(self.imageName)[0]
        self.offset = (size.x - first_sprite_width, size.y)

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

