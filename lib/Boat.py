import pygame
import math
import time
import csv 
from Buoy import *

class Boat(pygame.sprite.Sprite):
    def __init__(self,x,y,sailAngle):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/boat.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.x = x - 50
        self.y = y - 50
        self.vx = 0
        self.vy = 0
        self.distance = 0
        self.boatAngle = 10 #no. of deg boat rotated from horizontal
        self.sailAngle = sailAngle
        self.windDirection = 0
        self.lift = 2.5
        self.color = (0,0,0)
        self.x1 = x
        self.y1 = y + 25
        self.x2 = self.x1 + 55
        self.y2 = self.y1
        #self.imgWidth = self.imgHeight = 150
        
        self.moveSailCCW = False
        self.moveSailCW = False
        self.moveBoatCW = False
        self.moveBoatCCW = False
        
    def checkLimits(self): #Return False if sail > 90 degrees
        cBoatAngle = (90 - self.boatAngle)%360 #c = Compass frame of reference
        if cBoatAngle > 180: cBoatAngle -= 360 #Normalize to -180..0..180
        cSailAngle = (self.sailAngle + 90)%360
        if cSailAngle > 180: cSailAngle -= 360
        delta = cBoatAngle - cSailAngle
        minAngle = 10
        maxAngle = 89
        return minAngle < delta < maxAngle
    
    def updatePosition(self):
        #What changes with each keyboard input
        #360 degrees to normalize the respective angles
        if self.moveBoatCCW:
            self.boatAngle = (self.boatAngle-1)%360
            self.sailAngle = (self.sailAngle+1)%360
        elif self.moveBoatCW:
            self.boatAngle = (self.boatAngle+1)%360
            self.sailAngle = (self.sailAngle-1)%360
        elif self.moveSailCCW:
            self.sailAngle = (self.sailAngle-1)%360
        elif self.moveSailCW:
            self.sailAngle = (self.sailAngle+1)%360
        
        cBoatAngle = (90 - self.boatAngle)%360 #c = Compass frame of reference
        if cBoatAngle > 180: cBoatAngle -= 360 #Normalize to -180..0..180
        cSailAngle = (self.sailAngle + 90)%360
        if cSailAngle > 180: cSailAngle -= 360
        delta = cBoatAngle - cSailAngle
        if delta < -180: delta += 360
        tSailAngle = (-self.sailAngle) %360  #Trig frame of reference

        #Propulsion from lift. Max lift at 45 degrees, 0 at 90 & 180
        lift = abs(cSailAngle)
        if 45 < lift <= 90: lift = 90 - lift
        elif 90 < lift <= 135: lift = lift - 90
        elif lift > 135: lift = 180 - lift
        effectiveLift = self.lift * lift / 45.0 
        self.vx = abs(math.sin(math.radians(tSailAngle))* effectiveLift)
        if cBoatAngle<0: self.vx = -self.vx #pointing to the left
        #vy: positive is up, negative is down
        self.vy = abs(math.cos(math.radians(tSailAngle))* effectiveLift)
        if 45<cSailAngle<135 or -135<cSailAngle<-45: self.vy = -self.vy

        #Propulsion from push. Max at 90. 0 at <45.
        pushFactor = 0.4
        pushAngle = cSailAngle % 360
        if 45<pushAngle<90: pushFactor *= (pushAngle-45)/45.0
        elif 90<pushAngle<135: pushFactor *= (135-pushAngle)/45.0
        elif 225<pushAngle<270: pushFactor *= (pushAngle-225)/45.0
        elif 270<pushAngle<315: pushFactor *= (315-pushAngle)/45.0
        else: pushFactor *= 0.01 #just a slight push
        self.vy -= pushFactor #+ve is up

        #Drag from boat broadside
        dragFactor = 0.9
        horiDrag = abs(math.cos(math.radians(cBoatAngle))*dragFactor)
        vertDrag = abs(math.sin(math.radians(cBoatAngle))*dragFactor)
        if self.vx > 0:
            self.vx -= horiDrag
            if self.vx < 0: self.vx = 0 #drag cannot go beyond 0
        else:
            self.vx += horiDrag
            if self.vx > 0: self.vx = 0
        if self.vy > 0:
            self.vy -= vertDrag
            if self.vy < 0: self.vy = 0
        else:
            self.vy += vertDrag
            if self.vy > 0: self.vy = 0
            
        #Adding change in speed per second to current position
        self.x += self.vx
        self.x2 += self.vx
        self.y -= self.vy
        self.y2 -= self.vy
        
        self.rect.left = self.x
        self.rect.top = self.y
    
    def drawBoat(self,screen):
        self.image = pygame.image.load('images/boat.png').convert_alpha()
        self.image = pygame.transform.rotate(self.image,self.boatAngle)
        #self.rect = self.image.get_rect(center = self.rect.center)
        screen.blit(self.image,(self.x,self.y))
        
    def drawSail(self,screen):
        self.rect = self.image.get_rect(center = self.rect.center)
        #End and start coordinates of line used to draw sail
        self.x1, self.y1 = self.rect.center
        self.x2, self.y2 = self.rect.center
        length = 50 #Length of sail
        self.x2 -= length* math.cos(math.radians(self.sailAngle))
        self.y2 -= length* math.sin(math.radians(self.sailAngle))
        
        #arcRectLeft = self.x1 - 0.5*self.rect.width
        #arcRecTop = self.y1 - 0.5*self.rect.height
        #width = 0.5*self.rect.width
        #height = 0.5*self.rect.height
        
        #Create surface object for the arc
        #self.arcRect = (arcRectLeft,arcRecTop,width,height)
        #pygame.draw.arc(screen,self.color,self.arcRect,startA,stopA,1)
        thickness = 2
        pygame.draw.line(screen,(self.color),
                         (self.x2,self.y2),(self.x1,self.y1),thickness)
        
        
class AutoBoat(Boat):
    def __init__(self,x,y,sailAngle,level,index):
        Boat.__init__(self,x,y,sailAngle)
        self.loadAI(x,y,level,index)
        self.image = pygame.image.load('images/AIboat.png').convert_alpha()
        
    def drawBoat(self,screen):
        self.image = pygame.image.load('images/AIboat.png').convert_alpha()
        self.image = pygame.transform.rotate(self.image,self.boatAngle)
        #self.rect = self.image.get_rect(center = self.rect.center)
        screen.blit(self.image,(self.x,self.y))
        
    def loadAI(self,x,y,level,index):
        self.movements = []
        start = "data/levels/"
        data = csv.reader(open(start+str(level)+"/"+str(index)+".dat","rb"))
        for row in data:
            self.movements.append(row)
    
