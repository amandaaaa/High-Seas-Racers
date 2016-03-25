import pygame
import time
import csv

from Boat import *

class SceneBase(object):
    def __init__(self):
        #Initialize color values
        self.black = (0,0,0)
        self.white = (225,225,225)
        self.next = self
        self.path = "images/"
        
        #Common menu buttons
        self.buttonHover = pygame.image.load(self.path+"button.png")
        self.buttonImg = pygame.image.load(self.path+"button3.png")
   
    def timerFired(self):
        pass
    
    def processInput(self, events, pressed_keys):
        pass
    
    def buttonColor(self):
        imgWidth = 180
        imgHeight = 70
        (x,y) = pygame.mouse.get_pos()
        if x > self.xCoord and x < self.xCoord + imgWidth:
            if y > self.yCoord and y < self.yCoord + imgHeight:
                return self.buttonHover
        return self.buttonImg
    
    def drawReturnButton(self,screen):
        font = pygame.font.Font("data/font/BradBunR.ttf",40) #Font size = 40
        screen.blit(self.buttonColor(),(self.xCoord,self.yCoord))
        text = "Go Home"
        label = font.render(text,1,self.white)
        xAdj = 30
        yAdj = 25
        screen.blit(label,(self.xCoord+xAdj,self.yCoord+yAdj))
        
    def updateScreen(self,screen):
        self.drawReturnButton(screen)

    def switchToScene(self, next_scene):
        self.next = next_scene
    
    def terminate(self):
        self.switchToScene(None)

class TitleScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        #Button drawn on MS Word
        self.bgImg = pygame.image.load(self.path+"title.png")
        #Title contains images from http://sweetclipart.com/ and
        #http://www.pcola.com/
        
        #Main image coordinates
        self.bgX= 0
        self.bgY = 0
        
        #Button coordinates
        self.xBut1 = 300
        self.width = 180
        self.yBut1 = 360
        self.height = 70
        self.yBut2 = self.yBut1 + 70
        self.yBut3 = self.yBut2 + 70
        self.white = (225,225,225)

    def processInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.switchToScene(EasyRace())
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (self.x,self.y) = pygame.mouse.get_pos()
                if self.x > self.xBut1 and self.x < self.width + self.xBut1:
                    if self.y > self.yBut1 and self.y < self.height+self.yBut1:
                        self.switchToScene(TutorialMenuScene())
                    elif self.y > self.yBut2 and self.y<self.height+self.yBut2:
                        self.switchToScene((EasyRace()))
                    elif self.y > self.yBut3 and self.y<self.height+self.yBut3:
                        self.switchToScene(InstructionsScene())
    
    def buttonColor(self,num):
        (x,y) = pygame.mouse.get_pos()
        if x > self.xBut1 and x < self.width + self.xBut1:
            if y > self.yBut1 and y < self.height+self.yBut1 and num==1:
                return self.buttonHover
            elif y > self.yBut2 and y < self.height+self.yBut2 and num ==2:
                return self.buttonHover
            elif y > self.yBut3 and y < self.height+self.yBut3 and num ==3:
                return self.buttonHover
        return self.buttonImg
        
    def drawButtons(self,screen):
        #Tutorial button
        screen.blit(self.buttonColor(1),(self.xBut1,self.yBut1))
        font = pygame.font.Font("data/font/BradBunR.ttf",50)
        text1 = "Tutorial"
        label1 = font.render(text1,1,self.white)
        self.xAdj = self.xBut1 + 20
        self.yAdj = self.yBut1 + 20
        screen.blit(label1,(self.xAdj,self.yAdj))
        #Race button
        screen.blit(self.buttonColor(2),(self.xBut1, self.yBut2))
        text2 = "Race"
        label2 = font.render(text2,1,self.white)
        self.xAdj = self.xAdj + 30
        self.yAdj = self.yAdj + 70
        screen.blit(label2,(self.xAdj,self.yAdj))
        #Instructions button
        screen.blit(self.buttonColor(3),(self.xBut1,self.yBut3))
        font = pygame.font.Font("data/font/BradBunR.ttf", 30)
        text3 = "Instructions"
        label3 = font.render(text3,1,self.white)
        self.xAdj = self.xAdj - 28
        self.yAdj = self.yAdj + 80
        screen.blit(label3,(self.xAdj,self.yAdj))
    
    def updateScreen(self, screen):
        screen.fill((0, 128, 128))
        screen.blit(self.bgImg,(self.bgX,self.bgY))
        #screen.blit(label,(100,100))
        self.drawButtons(screen)
        
class TutorialMenuScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.buttonImg2 = pygame.image.load(self.path+"button2.png")
        #Buttons drawn on MS Word
        self.bgX = self.bgY = 0
        #Teeny level buttons
        self.butWidth = 50
        self.xBut1 = 120
        self.yBut1 = 200
        self.xBut2 = self.xBut1*2 + self.butWidth
        self.xBut3 = self.xBut1*3 + self.butWidth*2
        self.xBut4 = self.xBut1*4 + self.butWidth*3
        #Large return button
        self.but2Width = 180
        self.but2Height = 100
        self.xCoord = 600
        self.yCoord = 10
        
    def processInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.switchToScene(ReachDemo1())
                elif event.key == pygame.K_BACKSPACE:
                    self.switchToScene(TitleScene())
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (x,y) = pygame.mouse.get_pos()
                if y > self.yBut1 and y < self.yBut1 + self.butWidth:
                    if x > self.xBut1 and x < self.xBut1 + self.butWidth:
                        self.switchToScene(ReachDemo1())
                    elif x > self.xBut2 and x < self.xBut2 + self.butWidth:
                        self.switchToScene(ReachDemo2())
                    elif x > self.xBut3 and x < self.xBut3 + self.butWidth:
                        self.switchToScene(RunDemo())
                    elif x > self.xBut4 and x < self.xBut4 + self.butWidth:
                        self.switchToScene(UpwindDemo())
                elif x > self.xCoord and x < self.xCoord + self.but2Width:
                    if y > self.yCoord and y < self.yCoord + self.but2Height:
                        self.switchToScene(TitleScene())
                        
    def levelButColor(self,num):
        (x,y) = pygame.mouse.get_pos()
        self.hovImg = pygame.image.load(self.path+"button2.png")
        self.nonHovImg = pygame.image.load(self.path+"button4.png")
        if y > self.yBut1 and y < self.yBut1 + self.butWidth:
            if x > self.xBut1 and x < self.xBut1 + self.butWidth and num==1:
                return self.hovImg
            if x > self.xBut2 and x < self.xBut2 + self.butWidth and num==2:
                return self.hovImg
            if x > self.xBut3 and x < self.xBut3 + self.butWidth and num==3:
                return self.hovImg
            if x > self.xBut4 and x < self.xBut4 + self.butWidth and num==4:
                return self.hovImg
        return self.nonHovImg
                            
    def drawLevelButtons(self,screen):
        #Level 1
        screen.blit(self.levelButColor(1),(self.xBut1,self.yBut1))
        font = pygame.font.Font("data/font/BradBunR.ttf",58)
        text1 = "1"
        label1 = font.render(text1,1,self.white)
        self.xAdj = self.xBut1 + 20
        self.yAdj = self.yBut1 - 2
        screen.blit(label1,(self.xAdj,self.yAdj))
        
        #Level 2
        screen.blit(self.levelButColor(2),(self.xBut2,self.yBut1))
        text2 = "2"
        label2 = font.render(text2,1,self.white)
        self.xAdj = self.xBut2 + 20
        screen.blit(label2,(self.xAdj,self.yAdj))
        
        #Level 3
        screen.blit(self.levelButColor(3),(self.xBut3,self.yBut1))
        text3 = "3"
        label3 = font.render(text3,1,self.white)
        self.xAdj = self.xBut3 + 20
        screen.blit(label3,(self.xAdj,self.yAdj))
        
        #Level 4
        screen.blit(self.levelButColor(4),(self.xBut4,self.yBut1))
        text4 = "4"
        label4 = font.render(text4,1,self.white)
        self.xAdj = self.xBut4 + 20
        screen.blit(label4,(self.xAdj,self.yAdj))
        
    def updateScreen(self,screen):
        screen.fill((0,128,128))
        bg = pygame.image.load(self.path+"bg4.png")
        #From http://www.pcola.com/common/images/topWave.png
        screen.blit(bg,(0,0))
        self.drawLevelButtons(screen)
        SceneBase.updateScreen(self,screen)
        
class RaceMenuScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.white = (225,225,225)
        
    def processInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.switchToScene(TitleScene())
        
    def updateScreen(self,screen):
        font = pygame.font.Font("data/font/BradBunR.ttf",50)
        text = "Dead end :( Press Enter to reverse"
        label = font.render(text,1,self.white)
        screen.fill((0,128,128))
        screen.blit(label,(2,0))
        

class InstructionsScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.white = (225,225,225)
        #self.buttonImg2 = pygame.image.load(self.path+"button.png")
        
        #Large return button
        self.but2Width = 180
        self.but2Height = 100
        self.xCoord = 600
        self.yCoord = 10
        
        #Continue button
        self.xCoordC = 600
        self.yCoordC = 500
        
    def processInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.switchToScene(TitleScene())
                elif event.key == pygame.K_RETURN:
                    self.switchToScene(InstructionsScene2())
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (x,y) = pygame.mouse.get_pos()
                if x > self.xCoord and x < self.xCoord + self.but2Width:
                    if y > self.yCoord and y < self.yCoord + self.but2Height:
                        self.switchToScene(TitleScene())
                    elif y > self.yCoordC and y < self.yCoordC+self.but2Height:
                        self.switchToScene(InstructionsScene2())
                        
    def butColor(self):
        butWidth = 180
        (x,y) = pygame.mouse.get_pos()
        if x > self.xCoordC and x < self.xCoordC + butWidth:
            if y > self.yCoordC and y < self.yCoordC + butWidth:
                return self.buttonHover
        return self.buttonImg
    
    def drawButtons(self,screen):
        #Forward button
        self.font = pygame.font.Font("data/font/BradBunR.ttf",40)
        screen.blit(self.butColor(),(self.xCoordC,self.yCoordC))
        text = "Continue"
        label1 = self.font.render(text,1,self.white)
        xAdj = 30
        yAdj = 25
        screen.blit(label1,(self.xCoordC+xAdj,self.yCoordC+yAdj))
        
    def drawDirections(self,screen,delta):
        font = pygame.font.Font("data/font/BradBunR.ttf",50)
        xCoord = 150
        yCoord = 50
        text1 = "Move sail anticlockwise"
        text2 = "Move sail clockwise"
        text3 = "Move boat anticlockwise"
        text4 = "Move boat clockwise"
        label1 = font.render(text1,1,self.white)
        label2 = font.render(text2,1,self.white)
        label3 = font.render(text3,1,self.white)
        label4 = font.render(text4,1,self.white)
        screen.blit(label1,(xCoord,yCoord))
        screen.blit(label2,(xCoord,yCoord+delta))
        screen.blit(label3,(xCoord,yCoord+delta*2))
        screen.blit(label4,(xCoord,yCoord+delta*3))
        
    def drawInstructions(self,screen):
        #drawing buttons
        path = "images/arrows/"
        up = pygame.image.load(path+"up.png")
        down = pygame.image.load(path+"down.png")
        left = pygame.image.load(path+"left.png")
        right = pygame.image.load(path+"right.png")
        #Arrows from http://bulk2.destructoid.com/ul/user/
        #5/56001-227292-ArrowKeysjpg-620x.jpg
        xCoord = 30
        yCoord = 30
        delta = 120
        buttons = [up,down,left,right]
        for i in xrange(len(buttons)):
            image = buttons[i]
            screen.blit(image,(xCoord,yCoord))
            yCoord += delta
        self.drawDirections(screen,delta)
        
    def updateScreen(self,screen):
        screen.fill((0,128,128))
        bg = pygame.image.load(self.path+"bg4.png")
        screen.blit(bg,(0,0))
        self.drawInstructions(screen)
        self.drawButtons(screen)
        SceneBase.updateScreen(self,screen)
        
class InstructionsScene2(InstructionsScene):
    def __init__(self):
        InstructionsScene.__init__(self)
        #Back button
        self.xCoordB = 10
        self.yCoordB = self.yCoordC
        self.initX, self.initY, self.initAngle = (40,300,-90)
        self.boat = Boat(self.initX, self.initY, self.initAngle)

    def processInput(self, events, pressed_keys):
        InstructionsScene.processInput(self,events,pressed_keys)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.switchToScene(InstructionsScene())
                elif event.key == pygame.K_RETURN:
                    self.switchToScene(InstructionsScene3())
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (x,y) = pygame.mouse.get_pos()
                if x > self.xCoordB and x < self.xCoordB + self.but2Width:
                    if y>self.yCoordB and y <self.yCoordB+self.but2Height:
                        self.switchToScene(InstructionsScene())
                elif x > self.xCoordC and x < self.xCoordC+self.but2Width:
                    if y>self.yCoordB and y < self.yCoordB+self.but2Height:
                        self.switchToScene(InstructionsScene3())
    
    def timerFired(self):
        optimumAngle = -45
        demoWidth = 800
        if self.boat.sailAngle <= optimumAngle:
            self.boat.sailAngle += 1
        if self.boat.x <= demoWidth:
            self.boat.updatePosition()
            self.boat.x += 2 #force boat to move straight across screen
            self.boat.y = self.initY
        else: #restart boat movement
            self.boat.sailAngle = self.initAngle
            self.boat.x = self.initX
            
    def chooseColor(self):
        butWidth = 180
        (x,y) = pygame.mouse.get_pos()
        if x > self.xCoordB and x < self.xCoordB + butWidth:
            if y > self.yCoordC and y < self.yCoordC + butWidth:
                return self.buttonHover
        return self.buttonImg
                        
    def drawDemo(self,screen):
        img = pygame.image.load(self.path+"example.png")
        xCoord = 0
        yCoord = 140
        screen.blit(img,(xCoord,yCoord))
        self.boat.drawBoat(screen)
        self.boat.drawSail(screen)
        
    def drawInstructions(self,screen):
        text = "Aim: Propel your boat to the finish line with the wind's help!"
        font = pygame.font.Font("data/font/BradBunR.ttf",30)
        label = font.render(text,1,self.white)
        xCoord,yCoord = 80,100
        screen.blit(label,(xCoord,yCoord))
        self.drawDemo(screen)
    
    def drawButtons(self,screen):
        InstructionsScene.drawButtons(self,screen)
        #Back button
        screen.blit(self.chooseColor(),(self.xCoordB,self.yCoordB))
        text = "Back"
        label2 = self.font.render(text,1,self.white)
        xAdj = 50
        yAdj = 25
        screen.blit(label2,(self.xCoordB+xAdj,self.yCoordB+yAdj))
        SceneBase.updateScreen(self,screen)
        
class InstructionsScene3(InstructionsScene2):
    def __init__(self):
        InstructionsScene2.__init__(self)
        
    def processInput(self, events, pressed_keys):
        InstructionsScene.processInput(self,events,pressed_keys)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.switchToScene(InstructionsScene2())
                elif event.key == pygame.K_RETURN:
                    self.switchToScene(InstructionsScene4())
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (x,y) = pygame.mouse.get_pos()
                if x > self.xCoordB and x < self.xCoordB + self.but2Width:
                    if y>self.yCoordB and y <self.yCoordB+self.but2Height:
                        self.switchToScene(InstructionsScene2())
                elif x > self.xCoordC and x < self.xCoordC+self.but2Width:
                    if y>self.yCoordB and y < self.yCoordB+self.but2Height:
                        self.switchToScene(InstructionsScene4())
        
    def drawInstructions(self,screen):
        text = "These are the directions you can sail in:"
        font = pygame.font.Font("data/font/BradBunR.ttf",35)
        label = font.render(text,1,self.white)
        xCoord, yCoord = 140,100
        screen.blit(label,(xCoord,yCoord))
        img = pygame.image.load(self.path+"points.jpg")
        #Image from http://www.schoolofsailing.net/Images/points-of-sail.jpg
        xCoord, yCoord = 190,150
        screen.blit(img,(xCoord,yCoord))
        
class InstructionsScene4(InstructionsScene):
    def __init__(self):
        InstructionsScene.__init__(self)
        #Back button
        self.xCoordB = 10
        self.yCoordB = self.yCoordC
        self.font = pygame.font.Font("data/font/BradBunR.ttf",40)
        
    def processInput(self,events,pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.switchToScene(InstructionsScene3())
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (x,y) = pygame.mouse.get_pos()
                if x > self.xCoord and x < self.xCoord + self.but2Width:
                    if y > self.yCoord and y < self.yCoord + self.but2Height:
                        self.switchToScene(TitleScene())
                elif x > self.xCoordB and x < self.xCoordB + self.but2Width:
                    if y>self.yCoordB and y <self.yCoordB+self.but2Height:
                        self.switchToScene(InstructionsScene3())
                        
    def drawInstructions(self,screen):
        coord1 = (100,100)
        text1 = "Credits:"
        label1 = self.font.render(text1,1,self.white)
        screen.blit(label1,coord1)
        coord2 = (100,140)
        text2 = "Nick Wilson for his mentorship"
        label2 = self.font.render(text2, 1, self.white)
        screen.blit(label2,coord2)
        coord3=(100,180)
        text3 ="Python and Pygame"
        label3 = self.font.render(text3, 1, self.white)
        screen.blit(label3,coord3)
        coord4=(100,220)
        text4="Image credits in code files"
        label4 = self.font.render(text4, 1, self.white)
        screen.blit(label4,coord4)
        coord5=(100,260)
        text5="Scene structure from NerdParadise.com"
        label5 = self.font.render(text5, 1, self.white)
        screen.blit(label5,coord5)
        
    def chooseColor(self):
        butWidth = 180
        (x,y) = pygame.mouse.get_pos()
        if x > self.xCoordB and x < self.xCoordB + butWidth:
            if y > self.yCoordC and y < self.yCoordC + butWidth:
                return self.buttonHover
        return self.buttonImg
    
    def drawButtons(self,screen):
        #Back button
        screen.blit(self.chooseColor(),(self.xCoordB,self.yCoordB))
        text = "Back"
        label2 = self.font.render(text,1,self.white)
        xAdj = 50
        yAdj = 25
        screen.blit(label2,(self.xCoordB+xAdj,self.yCoordB+yAdj))
        
class DemoScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        #Background for the all demo scenes
        self.bg1 = pygame.image.load(self.path+'bg1.png').convert_alpha()
        self.bg2 = pygame.image.load(self.path+'bg2.png').convert_alpha()
        self.bg3 = pygame.image.load(self.path+'bg3.png').convert_alpha()
        #bg1,bg2,bg3.png done on MS Paint
        
        #Regarding boat and sail movement
        self.windDirection = 90 #degrees anticlockwise from horizontal
        
        #For displaying text on screen
        self.counter = 0
        self.message = False
        self.text = "FOLLOW ME! (Wind coming from top of screen)"
        
        #For allowing pushing and holding of keys
        self.boat.moveBoatCW = False
        self.boat.moveBoatCCW = False
        self.boat.moveSailCCW = False
        self.boat.moveSailCW = False
        
        #Checking finish
        self.finished = False
        self.nextScene = None
        self.loose = False
        
        #Large return button
        self.but2Width = 180
        self.but2Height = 100
        self.xCoord = 600
        self.yCoord = 10
        
        self.startTime = pygame.time.get_ticks()
        self.timeElapsed = pygame.time.get_ticks() - self.startTime
        self.boo = ""
        
    def processInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    #boat moves anticlockwise (sail moves on boat too)
                    self.boat.moveBoatCCW = True
                elif event.key == pygame.K_RIGHT:
                    #boat moves clockwise (sail moves on boat too)
                    self.boat.moveBoatCW = True
                elif event.key == pygame.K_UP:
                    #sail moves clockwise
                    self.boat.moveSailCCW = True
                elif event.key == pygame.K_DOWN:
                    #sail moves anticlockwise
                    self.boat.moveSailCW = True
                elif event.key == pygame.K_RETURN and self.finished:
                    self.switchToScene(self.nextScene)
                elif event.key == pygame.K_RETURN and self.loose:
                    self.switchToScene(TutorialMenuScene())
                    
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    #boat moves anticlockwise (sail moves on boat too)
                    self.boat.moveBoatCCW = False
                elif event.key == pygame.K_RIGHT:
                    #boat moves clockwise (sail moves on boat too)
                    self.boat.moveBoatCW = False
                elif event.key == pygame.K_UP:
                    #sail moves clockwise
                    self.boat.moveSailCCW = False
                elif event.key == pygame.K_DOWN:
                    #sail moves anticlockwise
                    self.boat.moveSailCW = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (x,y) = pygame.mouse.get_pos()
                if x > self.xCoord and x < self.xCoord + self.but2Width:
                    if y > self.yCoord and y < self.yCoord + self.but2Height:
                        self.switchToScene(TitleScene())
                        
    def timerFired(self):
        self.boat.updatePosition()
        self.checkFinish()
        self.checkLose()
        #Demo boat
        self.timeElapsed = pygame.time.get_ticks() - self.startTime
        path = self.autoBoat.movements
            
        if len(path) != 0 and self.timeElapsed > int(path[0][4]):
            self.autoBoat.x = float(path[0][0])
            self.autoBoat.y = float(path[0][1])
            self.autoBoat.boatAngle = float(path[0][2])
            self.autoBoat.sailAngle = float(path[0][3])
            if len(path)!= 0:
                 self.autoBoat.movements = path[1:]
        self.autoBoat.updatePosition()
                        
    def checkLose(self):                 
        x = self.boat.x 
        y = self.boat.y
        winXEnd = 750
        winXStart = -21
        winYEnd = 590
        winYStart = 10
        if x > winXEnd or x < winXStart or y > winYEnd or y<winYStart:
            if not self.finished:
                self.loose = True 
    
    def drawBG(self,screen):
        #3 images taking turns to be shown
        bgCoord = (0,0)
        bgTime = 30
        step = 30
        bgCounter = self.counter
        if bgCounter < bgTime:
            screen.blit(self.bg1,bgCoord)
        elif bgCounter < bgTime + step:
            screen.blit(self.bg2,bgCoord)
        elif bgCounter < bgTime + step*2:
            screen.blit(self.bg3,bgCoord)
        else:
            self.counter -= bgTime + step*2
        self.counter += 1
        
    def drawInstruct(self,screen):
        time = 90
        fontSize = 20
        labelPosition = (120,50)
        if self.counter < time and self.message == False:
            font = pygame.font.Font("data/font/BradBunR.ttf",fontSize)
            text = self.text
            label = font.render(text,1,self.black)
            screen.blit(label,labelPosition)
        if self.counter == time:
            self.message = True
            
    def drawWin(self,screen):
        if self.finished:
            xMsg, yMsg = (300,200)
            fontSize = 30
            text = "YOU HAVE FINISHED!"
            font = pygame.font.Font("data/font/BradBunR.ttf",fontSize)
            label = font.render(text,1,(self.white))
            screen.blit(label,(xMsg,yMsg))
            
    def drawBoat(self,screen):
        self.boat.drawBoat(screen)
        self.autoBoat.drawBoat(screen)
        
    def drawSail(self,screen):
        self.boat.drawSail(screen)
        self.autoBoat.drawSail(screen)
        
    def drawCongrats(self,screen):
        grat = pygame.image.load(self.path+'congrats.png').convert_alpha()
        if self.finished:
            vanish = 2000
            self.boat.x = self.boat.y = vanish
            coord = (10,30)
            screen.blit(grat,coord)
            
    def drawLoose(self,screen):
        lose = pygame.image.load(self.path+'lose.png').convert_alpha()
        if self.loose:
            vanish = 2000
            self.boat.x = self.boat.y = vanish
            coord = (10,40)
            screen.blit(lose,coord)
        
    def updateScreen(self,screen):
        self.drawBG(screen)
        self.drawInstruct(screen)
        self.drawStartEnd(screen)
        self.drawWin(screen)
        self.drawBoat(screen)
        self.drawSail(screen)
        self.drawCongrats(screen)
        self.drawLoose(screen)
        self.drawReturnButton(screen)
        pygame.display.update()
 
class ReachDemo1(DemoScene):
    def __init__(self):
        #Instantiate boat
        self.boat = Boat(30,180,-90)
        self.autoBoat = AutoBoat(30,240,-90,"tutorials",1)
        DemoScene.__init__(self)
        
        #Starting line
        self.xStart = 100
        self.xEnd = 700
        self.yTop = 10
        self.yBottom = 300
        
        self.nextScene = ReachDemo2()
        
    def processInput(self, events, pressed_keys):
        #Handle key and mouse press events
        for event in events:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    #sail moves clockwise
                    self.boat.moveSailCCW = False
                elif event.key == pygame.K_DOWN:
                    #sail moves anticlockwise
                    self.boat.moveSailCW = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    #sail moves clockwise
                    self.boat.moveSailCCW = True
                elif event.key == pygame.K_DOWN:
                    #sail moves anticlockwise
                    self.boat.moveSailCW = True
                elif event.key == pygame.K_RETURN and self.finished:
                    self.switchToScene(ReachDemo2())
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (x,y) = pygame.mouse.get_pos()
                if x > self.xCoord and x < self.xCoord + self.but2Width:
                    if y > self.yCoord and y < self.yCoord + self.but2Height:
                        self.switchToScene(TitleScene())
        
    def checkFinish(self):
        margin = 30
        if self.boat.x > self.xEnd and self.boat.y < self.yBottom + margin:
            self.finished = True
            return True
        return False
    
    def timerFired(self):
        self.boat.updatePosition()
        self.checkFinish()
        self.checkLose()
        #Demo boat
        self.timeElapsed = pygame.time.get_ticks() - self.startTime
        path = self.autoBoat.movements
            
        if len(path) != 0 and self.timeElapsed > int(path[0][4]):
            self.autoBoat.x = float(path[0][0])
            self.autoBoat.y = float(path[0][1])
            self.autoBoat.boatAngle = float(path[0][2])
            self.autoBoat.sailAngle = float(path[0][3])
            if len(path)!= 0:
                 self.autoBoat.movements = path[1:]
        self.autoBoat.updatePosition()
    
    def drawStartEnd(self,screen):
        thickness = 10
        #Start line
        (xStart, xEnd) = (self.xStart,self.xEnd)
        (yTop, yBottom) = (self.yTop,self.yBottom)
        pygame.draw.line(screen,(self.black),
                         (xStart,yTop),(xStart,yBottom),thickness)
        #Finish line
        pygame.draw.line(screen,(self.black),
                         (xEnd,yTop),(xEnd,yBottom),thickness)
        
        #Start line label
        fontSize = 20
        (xAdj, yAdj) = (15,20) #Make it centered where lines are
        font = pygame.font.Font("data/font/BradBunR.ttf",fontSize)
        text1 = "Start"
        label1 = font.render(text1,1,self.black)
        screen.blit(label1,(xStart-xAdj,yBottom+yAdj))
        
        #End line label
        (xAdj,yAdj) = (10, 20)
        text2 = "End"
        label2 = font.render(text2,1,self.black)
        screen.blit(label2,(xEnd-xAdj,yBottom+yAdj))
        
class ReachDemo2(DemoScene):
    def __init__(self):
        self.boat = Boat(50,180,-90)
        self.autoBoat = AutoBoat(30,240,-90,"tutorials",2)
        DemoScene.__init__(self)
        self.yBottom2 = 400
        self.yTop2 = 200
        self.xStart = 100
        self.xEnd = 700
        self.yTop = 100
        self.yBottom = 400
        self.text = "Now use right and left arrow keys to move boat"
        self.nextScene = RunDemo()

    def drawStartEnd(self,screen):
        #start line
        (xStart, xEnd) = (self.xStart,self.xEnd)
        (yTop, yBottom) = (self.yTop,self.yBottom)
        yTop2 = self.yTop2
        yBottom2 = self.yBottom2
        pygame.draw.line(screen,self.black,(xStart,yTop),(xStart,yBottom),10)
        #finish line
        pygame.draw.line(screen,self.black,(xEnd,yTop2),(xEnd,yBottom2),10)
        #start
        font = pygame.font.Font("data/font/BradBunR.ttf",20)
        text1 = "Start"
        label1 = font.render(text1,1,self.black)
        screen.blit(label1,(xStart-15,yBottom+20))
        #ends
        text2 = "End"
        label2 = font.render(text2,1,self.black)
        screen.blit(label2,(xEnd-10,yBottom+20))
     
    def checkFinish(self):
        bottomMargin = 100
        topMargin = 100
        if self.boat.x > self.xEnd and self.boat.y > self.yTop2-topMargin:
            if self.boat.y < self.yBottom2-bottomMargin:
                self.finished = True
                return True
        return False

class RunDemo(DemoScene):
    def __init__(self):
        self.boat = Boat(300,80,10)
        self.autoBoat = AutoBoat(400,80,-90,"tutorials",3)
        DemoScene.__init__(self)
        #Start and ending coordinates
        self.xStart = 200
        self.xEnd = 600
        self.yStart = 400
        self.yEnd = 200
        self.margin = 40
        #Can only finish the race if has started
        self.started = False
        self.nextScene = UpwindDemo()
        
    def checkStarted(self):
        margin = self.margin
        if self.boat.x > self.xStart - margin:
            if self.boat.x < self.xEnd + margin:
                if self.boat.y > self.yStart:
                    self.started = True
    
    def checkFinish(self):
        margin = self.margin
        self.checkStarted()
        if self.started:
            if self.boat.y > self.yEnd:
                if self.boat.x > self.xStart - margin:
                    if self.boat.x < self.xEnd + margin:
                        self.finished = True
                        return True
        return False
        
    def drawStartEnd(self,screen):
        xStart = self.xStart
        xEnd = self.xEnd
        yStart = self.yStart
        yEnd = self.yEnd
        #start line
        pygame.draw.line(screen,self.black,(xStart,yStart),(xEnd,yStart),10)
        #finish line
        pygame.draw.line(screen,self.black,(xStart,yEnd),(xEnd,yEnd),10)
        #start label
        font = pygame.font.Font("data/font/BradBunR.ttf",20)
        text1 = "End"
        label1 = font.render(text1,1,self.black)
        screen.blit(label1,(xStart-self.margin,yStart))
        #end label
        text2 = "Start"
        label2 = font.render(text2,1,self.black)
        screen.blit(label2,(xStart-self.margin,yEnd))
        
class UpwindDemo(RunDemo):
    #Just making user move boat in the opposite direction to running
    def __init__(self):
        self.boat = Boat(300,500,10)
        self.autoBoat = AutoBoat(400,550,10,"tutorials",4)
        DemoScene.__init__(self)
        #Start and ending coordinates
        self.xStart = 200
        self.xEnd = 600
        self.yStart = 200
        self.yEnd = 400
        self.margin = 20
        #Can only finish the race if has started
        self.started = False
        self.nextScene = TitleScene()
        
    def checkStarted(self):
        margin = self.margin
        if self.boat.x > self.xStart - margin:
            if self.boat.x < self.xEnd + margin:
                if self.boat.y < self.yStart:
                    self.started = True
                    
    def checkFinish(self):
        margin = self.margin
        self.checkStarted()
        if self.started:
            if self.boat.y < self.yEnd:
                if self.boat.x > self.xStart - margin:
                    if self.boat.x < self.xEnd + margin:
                        self.finished = True
                        return True
        return False
        
    def drawStartEnd(self,screen):
        xStart = self.xStart
        xEnd = self.xEnd
        yStart = self.yStart
        yEnd = self.yEnd
        #start line
        pygame.draw.line(screen,self.black,(xStart,yStart),(xEnd,yStart),10)
        #finish line
        pygame.draw.line(screen,self.black,(xStart,yEnd),(xEnd,yEnd),10)
        #start label
        font = pygame.font.Font("data/font/BradBunR.ttf",20)
        text1 = "End"
        label1 = font.render(text1,1,self.black)
        screen.blit(label1,(xStart-self.margin,yStart))
        #end label
        text2 = "Start"
        label2 = font.render(text2,1,self.black)
        screen.blit(label2,(xStart-self.margin,yEnd))

class EasyRace(DemoScene):
    
    buoyList = []
    autoBoats = []
    
    def __init__(self):
        #Player's boat
        EasyRace.buoyList = []
        EasyRace.autoBoats = []
        self.boat = Boat(50,150,-90)
        DemoScene.__init__(self)
        
        #AI Boats
        autoBoat1 = AutoBoat(50,300, -90,1,1)
        EasyRace.autoBoats.append(autoBoat1)
        autoBoat2= AutoBoat(50,230,-90,1,3)
        EasyRace.autoBoats.append(autoBoat2)
        
        #Start and ending coordinates
        self.xStart = 100
        self.yStart = 100
        self.yEnd = 500
        
        #Create new buoys
        buoy1 = Buoy(600,200,False,True,False,True)
        EasyRace.buoyList.append(buoy1)
        buoy2 = Buoy(400,450,True,False,True,True)
        EasyRace.buoyList.append(buoy2)
        
        self.started = False
        self.finished = False
        self.nextScene = TitleScene()
        
        self.text = "Let's go!"
        
    def timerFired(self):
        #Store old position in case of collision
        self.oldX = self.boat.x
        self.oldY = self.boat.y
        self.boat.updatePosition()
        self.checkCollide()
        self.checkFinish()
        for autoBoat in EasyRace.autoBoats:
            autoBoat.updatePosition()
            
        #For autoboats
        for boat in xrange(len(EasyRace.autoBoats)):
            self.timeElapsed = pygame.time.get_ticks() - self.startTime
            path = EasyRace.autoBoats[boat].movements
            
            if len(path) != 0 and self.timeElapsed > int(path[0][4]):
                EasyRace.autoBoats[boat].x = float(path[0][0])
                EasyRace.autoBoats[boat].y = float(path[0][1])
                EasyRace.autoBoats[boat].boatAngle = float(path[0][2])
                EasyRace.autoBoats[boat].sailAngle = float(path[0][3])
                if len(path)!= 0:
                     EasyRace.autoBoats[boat].movements = path[1:]

    def processInput(self, events, pressed_keys):
        DemoScene.processInput(self,events,pressed_keys)
 
    def checkStarted(self): #check if boat crossed start line
        margin = 50
        if not self.started:
            if self.boat.x > self.xStart:
                if self.boat.y > self.yStart - margin:
                    if self.boat.y < self.yStart + margin:
                        self.started = True
                        
    def checkFinished(self): #check if boat crossed finish line
        margin = 50
        if self.boat.x < self.xStart:
            if self.boat.y > self.yStart - margin:
                if self.boat.y < self.yEnd + margin:
                    return True
        return False
    
    def checkFinish(self): #wrapper function for mark rounding and finishing
        margin = 50
        self.checkStarted()
        if self.started:
            for buoys in EasyRace.buoyList:
                if buoys.hasRounded(self.boat.x,self.boat.y) == False:
                    return False
            if self.checkFinished():
                self.finished = True
                return True

    def checkCollide(self):
        for buoy in EasyRace.buoyList:
            if pygame.sprite.collide_rect(buoy,self.boat):
                self.boat.x = self.oldX
                self.boat.y = self.oldY
        for autoboat in EasyRace.autoBoats:
            if pygame.sprite.collide_rect(autoboat,self.boat):
                self.boat.x = self.oldX
                self.boat.y = self.oldY
 
    def drawStartEnd(self,screen):
        xStart = self.xStart
        yStart = self.yStart
        yEnd = self.yEnd
        thick = 10
        #start and finish line same
        if self.started:
            color = (0,255,0) #green
        else:
            color = self.black
        pygame.draw.line(screen,color,(xStart,yStart),(xStart,yEnd),thick)
  
    def drawBuoys(self,screen):
        for i in xrange(len(EasyRace.buoyList)):
            buoy = EasyRace.buoyList[i]
            buoy.drawBuoy(screen,i)

    def drawBoat(self,screen):
        self.boat.drawBoat(screen)
        for autoBoat in EasyRace.autoBoats:
            autoBoat.drawBoat(screen)
  
    def drawSail(self,screen):
        self.boat.drawSail(screen)
        for autoBoat in EasyRace.autoBoats:
           autoBoat.drawSail(screen)
    
    def updateScreen(self,screen): 
        self.drawBG(screen)
        self.drawInstruct(screen)
        self.drawStartEnd(screen)
        self.drawWin(screen)
        self.drawBoat(screen)
        self.drawLoose(screen)
        self.drawSail(screen)
        self.drawBuoys(screen)
        self.drawReturnButton(screen)
        pygame.display.update()
   
