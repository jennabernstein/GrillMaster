import pygame
from engines import GameEngine
from UI import ScreenManager
from utils import RESOLUTION, UPSCALED

def main():
    #Initialize the module
    pygame.init()
    
    pygame.font.init()
    
    
    #Get the screen
    screen = pygame.display.set_mode(list(map(int, UPSCALED)))
    drawSurface = pygame.Surface(list(map(int, RESOLUTION)))

    screenManager = ScreenManager()
    gameEngine = GameEngine()
    
    RUNNING = True
    
    while RUNNING:
        screenManager.draw(drawSurface)
        
        pygame.transform.scale(drawSurface,
                               list(map(int, UPSCALED)),
                               screen)
     
        pygame.display.flip()
        gameClock = pygame.time.Clock()
        
        
        # event handling, gets all event from the eventqueue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                # change the value to False, to exit the main loop
                RUNNING = False
            else:
                screenManager.handleEvent(event)
        
        gameClock.tick(60)
        seconds = gameClock.get_time() / 1000
        screenManager.update(seconds)
     
    pygame.quit()


if __name__ == '__main__':
    main()