import pygame

from lib.Scenes import *

def runGame(width, height, fps, startingScene):
    pygame.init() #initialize Pygame
    screen = pygame.display.set_mode((width, height)) 
    clock = pygame.time.Clock()
    
    #Set icon to Snoopy sailing
    icon = pygame.image.load('images/snoopy.jpg')
    pygame.display.set_icon(icon)  #Set game icon
    #snoopy.jpg frm https://thisisnotadvertising.wordpress.com/tag/snoopy/
    
    #Set title to Cheesy title
    title = "High Seas Racers"
    pygame.display.set_caption(title)

    activeScene = startingScene

    while activeScene != None:
        pressedKeys = pygame.key.get_pressed()
        
        # Event filtering 
        filteredEvents = []
        for event in pygame.event.get():
            #Key combinations that user can use to exit game
            quitAttempt = False
            if event.type == pygame.QUIT:
                quitAttempt = True
            elif event.type == pygame.KEYDOWN:
                altPressed = pressedKeys[pygame.K_LALT] or \
                              pressedKeys[pygame.K_RALT]
                if event.key == pygame.K_ESCAPE:
                    quitAttempt = True
                elif event.key == pygame.K_F4 and altPressed:
                    quitAttempt = True
            if quitAttempt:
                activeScene.terminate()
            else:
                filteredEvents.append(event)
        activeScene.timerFired()
        activeScene.processInput(filteredEvents, pressedKeys)
        activeScene.updateScreen(screen)
        
        activeScene = activeScene.next
        
        pygame.display.flip()
        clock.tick(fps) 

runGame(800, 600, 30, TitleScene())

#Scene formatting taken from
#http://www.nerdparadise.com/tech/python/pygame/basics/part7/

#Images and soundtrack in video cited in Youtube description