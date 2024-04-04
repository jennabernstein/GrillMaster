"""
A Singleton Sprite Manager class
Author: Liz Matthews, 7/21/2023

Provides on-demand loading of images for a pygame program.
Will load entire sprite sheets if given an offset.

"""

from pygame import image, Surface, Rect, SRCALPHA
from os.path import join
import pygame

class SpriteManager(object):
   """A singleton factory class to create and store sprites on demand."""
   
   # The singleton instance variable
   _INSTANCE = None
   
   @classmethod
   def getInstance(cls):
      """Used to obtain the singleton instance"""
      if cls._INSTANCE == None:
         cls._INSTANCE = cls._SM()
      
      return cls._INSTANCE
   
   # Do not directly instantiate this class!
   class _SM(object):
      """An internal SpriteManager class to contain the actual code. Is a private class."""
      
      # Folder in which images are stored
      _IMAGE_FOLDER = "images"
      
      # Static information about the sprite sizes of particular image sheets.
      _SPRITE_SIZES = {
         "chef sprite.png" : (20, 40),
         "trash cans.png" : (85, 165),
         "food/patties.png" : (90, 90),
         "food/lettuce and cheese.png" : (100, 90),
         "food/onions.png" : (90, 90),
         "food/tomatos.png" : (107, 90),
         "food/patty.png" : (90, 70),
         "food/burger sprites.png" : (90,90),
         "food/burger bun.png" : (300,250),
         "food/plate.png" : (300,300),
         "food/burger/bun.png": (20,20), 
         "food/burger/cheese and tomato.png": (20,20), 
         "food/burger/cheese, tomato, lettuce.png": (50,50), 
         "food/burger/cheese.png": (50,50), 
         "food/burger/lettuce and cheese.png": (50,50), 
         "food/burger/lettuce and tomato.png": (50,50), 
         "food/burger/lettuce.png": (50,50), 
         "food/burger/patty.png": (20,20), 
         "food/burger/tomato.png": (50,50),
         "food/hot dog/hot dog plate.png": (270,200),
         "food/hot dog/hot dog bun plate.png": (270,200),
         "customer1.png": (117, 238),
         "customer2.png": (117, 238),
         "customer3.png": (117, 238),
         "customer4.png": (117, 238),
         "cola machine.png": (163,194)
      }
      
      
      # A default sprite size
      _DEFAULT_SPRITE = (20, 40)
      
      # A list of images that require to be loaded with transparency
      _TRANSPARENCY = ["pink counter.png", "pink prep.png", "food/patties.png", "pink long counter.png", "trash cans.png", "food/tomatos.png",
                       "food/lettuce and cheese.png", "food/patty.png", "food/tomato.png", "food/lettuce.png", "food/cheese.png", "food/burger bun.png", "food/plate.png",
                       "food/burger/bun with plate.png", "food/burger/cheese and tomato with plate.png", "food/burger/cheese, tomato, lettuce with plate.png", "food/burger/cheese with plate.png", "food/burger/lettuce and cheese with plate.png", "food/burger/lettuce and tomato with plate.png", "food/burger/lettuce with plate.png", "food/burger/patty with plate.png", "food/burger/tomato with plate.png",
                       "tickets/ticket - meat patty.png", "tickets/ticket - meat patty, cheese.png", "tickets/ticket - meat patty, lettuce, cheese.png", "tickets/ticket - meat patty, tomato, lettuce.png", "tickets/ticket - meat patty, lettuce.png", "tickets/ticket - meat patty, tomato, cheese.png", "tickets/ticket - meat patty, tomato, lettuce.png", "tickets/ticket - meat patty, tomato.png",
                       "tickets/ticket - vegan patty.png", "tickets/ticket - vegan patty, cheese.png", "tickets/ticket - vegan patty, lettuce, cheese.png", "tickets/ticket - vegan patty, tomato, lettuce.png", "tickets/ticket - vegan patty, lettuce.png", "tickets/ticket - vegan patty, tomato, cheese.png", "tickets/ticket - vegan patty, tomato, lettuce.png", "tickets/ticket - vegan patty, tomato.png",
                       "food/burger/cheese without patty.png", "food/burger/lettuce without patty.png", "food/burger/tomato without patty.png", "food/burger/cheese, tomato without patty.png", "food/burger/cheese, tomato, lettuce without patty.png", "food/burger/lettuce, cheese without patty.png", "food/burger/lettuce, tomato without patty.png",
                       "food/hot dog/burnt hot dog meat.png", "food/hot dog/cooked hot dog meat.png", "food/hot dog/hot dog meat.png", "food/hot dog/cooked hot dog with plate.png", "food/hot dog/hot dog bun plate.png", "food/hot dog/hot dog bun.png", "food/hot dog/hot dog plate.png", "food/hot dog/cooked hot dog with plate.png", "food/hot dog/hot dog bun with plate.png",
                       "customer1.png", "customer2.png", "customer3.png", "customer4.png", "cola machine.png", "food/cola.png"]

      
      # A list of images that require to be loaded with a color key
      _COLOR_KEY = ["chef sprite.png", "trash.png",  "food/burger sprites.png",
                    "food/burger/bun.png", "food/burger/cheese and tomato.png", "food/burger/cheese, tomato, lettuce.png", "food/burger/cheese.png", "food/burger/lettuce and cheese.png", "food/burger/lettuce and tomato.png", "food/burger/lettuce.png", "food/burger/patty.png", "food/burger/tomato.png"]
      
      
      def __init__(self):
         # Stores the surfaces indexed based on file name
         # The values in _surfaces can be a single Surface
         #  or a two dimentional grid of surfaces if it is an image sheet
         self._surfaces = {}      
      
      def __getitem__(self, key):
         return self._surfaces[key]
   
      def __setitem__(self, key, item):
         self._surfaces[key] = item
      
      def getSize(self, fileName):
         spriteSize = SpriteManager._SM._SPRITE_SIZES.get(fileName,
                                             SpriteManager._SM._DEFAULT_SPRITE)
         return spriteSize
      
      def getSprite(self, fileName, offset=None, scale = 1, flip_x = False):
         # If this sprite has not already been loaded, load the image from memory
         if fileName not in self._surfaces.keys():
            self._loadImage(fileName, offset is not None, 0, 0)

         # If this is an image sheet, return the correctly offset sub-surface
         if offset is not None:
            original_surface = self[fileName][offset[1]][offset[0]]
            scaled_surface = pygame.transform.scale(
                  original_surface,
                  (
                     int(original_surface.get_width() * scale),
                     int(original_surface.get_height() * scale),
                  ),
            )
            if flip_x:
               scaled_surface = pygame.transform.flip(scaled_surface, True, False)
               return scaled_surface
            return scaled_surface

         # Otherwise, return the sheet created
         return self[fileName]
      
      def _loadImage(self, fileName, sheet=False, border_padding=0, shape_padding=0):
         # Load the full image
         fullImage = image.load(join(SpriteManager._SM._IMAGE_FOLDER, fileName))

         # Look up some information about the image to be loaded
         transparent = fileName in SpriteManager._SM._TRANSPARENCY
         colorKey = fileName in SpriteManager._SM._COLOR_KEY

         # Detect if transparency is needed
         if transparent:
            fullImage = fullImage.convert_alpha()
         else:
            fullImage = fullImage.convert()

         # If the image to be loaded is an image sheet, split it up based on the sprite size
         if sheet:
            self[fileName] = []

            # Try to get the sprite size, use the default size if it is not stored
            spriteSize = self.getSize(fileName)

            # See how big the sprite sheet is
            sheetDimensions = fullImage.get_size()

            # Iterate over the entire sheet, increment by the sprite size
            for y in range(0, sheetDimensions[1], spriteSize[1]):
               self[fileName].append([])
               count = 0
               for x in range(border_padding, sheetDimensions[0], spriteSize[0] + shape_padding):
                  # Calculate size with border padding only for the first sprite
                  size = (spriteSize[0], spriteSize[1])
                  # If we need transparency
                  if transparent:
                        sprite = Surface(size, SRCALPHA, 32)
                  else:
                        sprite = Surface(size)

                  sprite.blit(fullImage,(0,0), Rect((x, y), size))

                  # If we need to set the color key
                  if colorKey:
                        sprite.set_colorkey(sprite.get_at((shape_padding, shape_padding)))

                  # Add the sprite to the end of the current row
                  self[fileName][-1].append(sprite)
                  count += 1

         else:
            # Not a sprite sheet, the full image is what we wish to store
            self[fileName] = fullImage

            # If we need to set the color key
            if colorKey:
                  self[fileName].set_colorkey(self[fileName].get_at((0, 0)))
