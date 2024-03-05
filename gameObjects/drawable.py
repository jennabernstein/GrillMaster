from utils import SpriteManager, SCALE, RESOLUTION, vec

import pygame

class Drawable(object):
    
    CAMERA_OFFSET = vec(0,0)
    
    @classmethod
    def updateOffset(cls, trackingObject, worldSize):
        
        objSize = trackingObject.getSize()
        objPos = trackingObject.position
        
        offset = objPos + (objSize // 2) - (RESOLUTION // 2)
        
        for i in range(2):
            offset[i] = int(max(0,
                                min(offset[i],
                                    worldSize[i] - RESOLUTION[i])))
        
        cls.CAMERA_OFFSET = offset
        
        

    @classmethod    
    def translateMousePosition(cls, mousePos):
        newPos = vec(*mousePos)
        newPos /= SCALE
        newPos += cls.CAMERA_OFFSET
        
        return newPos
    
    def __init__(self, position=vec(0,0), fileName="", offset=None, scale=1):
        
        self.image = None
        self.fileName = fileName
        if fileName != "":
            self.image = SpriteManager.getInstance().getSprite(fileName, offset)
            self.image = pygame.transform.scale(self.image, (int(self.image.get_size()[0]*scale), int(self.image.get_size()[1]*scale)))

        self.position=vec(*position)
        self.imageName = fileName
        if self.image:
            self.rect = pygame.Rect(self.position[0], self.position[1], self.image.get_width(), self.image.get_height())
        self.stateType = None
        self.offset = 0


    
    def draw(self, drawSurface):
      drawSurface.blit(self.image, list(map(int, self.position - Drawable.CAMERA_OFFSET)))
            
    def change_offset(self,new_offset):
        if self.fileName != "":
            self.image = SpriteManager.getInstance().getSprite(self.fileName, new_offset)

    def getSize(self):
        return vec(*self.image.get_size())
    
    def handleEvent(self, event):
        pass
    
    def update(self, seconds):
        pass

    def chefOffsetPos(self, pos):
        return pos
    
    def collide(self,position):
        if self.rect.collidepoint(position):
            return True
        
    def scale(self, new_size):
        scaled_image = pygame.transform.scale(self.image, new_size)
        self.image = scaled_image

    def getStateType(self):
        if self.stateType:
            return self.stateType