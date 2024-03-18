from gameObjects import Drawable
import pygame
import os

class TextEntry(Drawable):   
    if not pygame.font.get_init():
        pygame.font.init()
    
    FONT_FOLDER = "fonts" 
    DEFAULT_FONT = "PressStart2P.ttf"
    DEFAULT_SIZE = 30
    FONTS = {
       "default" : pygame.font.Font(os.path.join(FONT_FOLDER,
                                    DEFAULT_FONT), DEFAULT_SIZE),
       "default8" : pygame.font.Font(os.path.join(FONT_FOLDER,
                                    DEFAULT_FONT), 8)
    }
  
    def __init__(self, position, text, font="default", size=DEFAULT_SIZE,
              color=(0,0,0)):
        super().__init__(position, "")
        self.color = color
        
        self.image = TextEntry.FONTS[font].render(text, False, self.color)