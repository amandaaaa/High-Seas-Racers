import pygame

class Buoy(pygame.sprite.Sprite):
    def __init__(self,x,y,n,s,e,w):
        #x and y coordinates of buoy center
        self.x = x 
        self.y = y
        self.radius = 15
        
        #Possible buoy colors
        self.red = (255,0,0) #red
        self.green = (0,255,0) #green
        self.white = (0,0,0)
        self.rounded = False
        
        #Compass lines surrounding buoy for rounding detection
        #n,s,e,w contain either True or False. If False, boat must pass that
        #compass line before he is considered to have rounded the mark
        self.north = n
        self.south = s
        self.east = e
        self.west = w
                
        #Create rect for collision detection
        self.diam = 2*self.radius
        self.left = x - self.radius
        self.top = y - self.radius
        self.rect = pygame.Rect(self.left, self.top, self.diam, self.diam)
  
    def hasRounded(self,xB,yB): #check whether user has rounded a buoy
        #4 imaginary lines from buoy. If boat passes through a pre-determined
        #set of lines, he has rounded the buoy
        #All rounding is done in a clockwise direction
        margin = 40 #Account for blank space in boat image
        if not self.north: #Required to pass northern line
            if xB >= self.x and yB <= self.y + margin: #Passed northen line
                self.north = True
        if not self.south:
            if xB <= self.x and yB >= self.y - margin: 
                self.south = True
        if not self.east:
            if xB >= self.x - margin and yB >= self.y:
                self.east = True
        if not self.west:
            if xB <= self.x + margin and yB >= self.y:
                self.west = True
        #Return True if required buoy is rounded
        if self.north and self.south and self.east and self.west:
            self.rounded = True
            return True
        return False
    
    def drawBuoy(self,screen,i):
        if self.rounded == True:
            color = self.green
        else:
            color = self.red
        pygame.draw.circle(screen,color,(self.x,self.y),self.radius,0)
        text = str(i+1)
        fontSize = 30
        deltaX = 5
        deltaY = 15
        font = pygame.font.Font("data/font/BradBunR.ttf",fontSize)
        label = font.render(text,1,(self.white))
        screen.blit(label,(self.x-deltaX,self.y-deltaY))
        