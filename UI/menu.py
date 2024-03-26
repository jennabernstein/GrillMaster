from gameObjects import Drawable
from utils.vector import vec, magnitude
from . import TextEntry

import pygame

class AbstractMenu(Drawable):
    def __init__(self, background, fontName="default",
                 color=(255,255,255)):
        super().__init__((0,0), background)
           
        self.options = {}
        self.additional_text = []  # Collection to store additional text
        
        self.color = color      
        self.font = fontName
     
    def addOption(self, key, text, position, center=None, color=(255,255,255)):
        self.options[key] = TextEntry(position, text, self.font, color)
        optionSize = self.options[key].getSize()
        if center != None:
            if center == "both":
                offset = optionSize // 2
            elif center == "horizontal":
                offset = vec(optionSize[0] // 2, 0)
            elif center == "vertical":
                offset = vec(0, optionSize[1] // 2)
            else:
                offset = vec(0,0)
            
            self.options[key].position -= offset
 
    def draw(self, surface):
        super().draw(surface)
        
        for item in self.options.values():
            item.draw(surface)
        
        # Draw additional text
        for text_entry in self.additional_text:
            text_entry.draw(surface)
    
    def addText(self, text, position, size, center=None, color=(255,255,255)):
        text_entry = TextEntry(position, text, self.font, color)
        if center != None:
            if center == "both":
                offset = size // 2
            elif center == "horizontal":
                offset = vec(size // 2, 0)
            elif center == "vertical":
                offset = vec(0, size // 2)
            else:
                offset = vec(0,0)
        text_entry.position -= offset
        
        # Add the text_entry to the collection
        self.additional_text.append(text_entry)



class EventMenu(AbstractMenu):
    def __init__(self, background, fontName="default",
                color=(255,255,255)):
        super().__init__(background, fontName, color)      
        self.eventMap = {}
     
    def addOption(self, key, text, position, eventLambda, center=None, color=(255,255,255)):
        super().addOption(key, text, position, center, color)      
        self.eventMap[key] = eventLambda
    
    def handleEvent(self, event):      
        for key in self.eventMap.keys():
            function = self.eventMap[key]
            if function(event):
                return key
    
    
    
        
        

