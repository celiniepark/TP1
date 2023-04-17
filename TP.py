from cmu_graphics import *
import math, copy
from PIL import Image
import os, pathlib
import random
# not  sure how exactly to "cite" but I referenced parts of the cmugraphicsdemos
# https://ernestoam.fandom.com/wiki/Category:Plants_vs._Zombies_2

class Sun:
    def __init__(self, sunlight, x, y):
        self.sunlight = sunlight
        self.sunWidth, self.sunHeight = 35, 35
        self.sunSpawnX = x
        self.sunSpawnY = y
    def sunFall(self, sunSpawnY):
        self.sunSpawnY += 10
    def pickUp(self, sunlight, newSun):
        self.sunlight += 25

#zombie class   
class Zombie:
    def __init__(self, speed):
        self.speed = speed
        # self.zWidth = width
        # self.zHeight = height
    
class Norm(Zombie):
    def __init__(self, speed):
        super().__init__(speed)

class Cone(Zombie):
    def __init__(self, speed):
        super().__init__(speed)

#plant class
class Plant:
    def __init__(self, health):
        self.health = health

def onAppStart(app):
    app.width = 1000
    app.height = 600
    app.cx = app.width/2
    app.cy = app.height/2
    app.timeUntilSun = 50
    # -------screens-------
    # title screen
    app.titleImage = openImage("../pvz_title.png")
    app.titleImageWidth,app.titleImageHeight = 1000, 600
    app.titleImage = CMUImage(app.titleImage)
    app.onTitle = True
    app.gameStart = False
    # direction screen
    app.directions = False
    # background screen
    app.bgImage = openImage("../pvz_house.png")
    app.bgImageWidth,app.bgImageHeight = 1000, 600
    app.bgImage = CMUImage(app.bgImage)
    app.onBackground = False
    # start screen
    app.gameStart = False
    app.wave = 1
    # menu screen
    app.onMenu = False
    # sun
    app.sun = openImage('../pvz_sun.png')
    app.sunImg = CMUImage(app.sun)
    app.sun = Sun(75,0,40)
    app.sunList = []

    app.zombie = openImage('../normZomb.png')
    app.zombieImg = CMUImage(app.zombie)
    app.zombWidth, app.zombHeight = 70, 120
    app.zombie = Zombie(5)
    # app.coneZombie = openImage()

def gameStart(app):
    app.gameStart = True
    app.wave = 1
    app.startingSun = 75
    app.sunList = []
def openImage(fileName):
   return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))

def onStep(app):
    # sun spawn and fall
    if app.onBackground == True and app.timeUntilSun > 0:
        app.timeUntilSun -= 1
    elif app.timeUntilSun == 0:
        app.timeUntilSun = 50
    # for sun in range(len(app.sunList)):
    #     if app.timeUntilSun % 20 == 0:
    #         app.sunList[sun].sunSpawnY += 10
def redrawAll(app):
    if app.onTitle == True:
        drawImage(app.titleImage, 0, 0, width=app.titleImageWidth, height=app.titleImageHeight)
        drawLabel('Press "D" for directions!', 925, 570, fill = 'cornSilk')
    elif app.directions == True:
        drawRect(0, 0, 1000, 600, fill='brown')
        drawLabel('Directions', 500, 50, size=40, fill='cornSilk')
        drawLabel("1. Don't let the zombies reach your house!", 500, 100, size=20, fill='cornSilk')
        drawLabel("2. Use plants to damage and block the zombies!", 500, 150, size=20, fill='cornSilk')
        drawLabel("3. You need sunlight to buy plants!", 500, 200, size=20, fill='cornSilk')
        drawLabel("3. Use Wall-Nuts as a defensive shield!", 500, 250, size=20, fill='cornSilk')
        drawLabel('Press "B" to return to the title screen', 500, 550, size=20, fill='cornSilk')
    elif app.gameStart == True:
        drawImage(app.bgImage, 0, 0, width=app.bgImageWidth, height=app.bgImageHeight)
        drawRect(0, 0, 120, 400, fill='sienna',  border='black', borderWidth=2)
        drawLine(2, 110, 118, 110, fill='saddleBrown', lineWidth=2)
        drawCircle(60, 40, 30, fill='peru', border='saddleBrown', borderWidth=2)
        drawImage(app.sunImg, 60, 40, width=app.sun.sunWidth, height=app.sun.sunHeight, align='center')
        drawRect(60, 85, 70, 20, fill='blanchedAlmond', border='black', borderWidth=1, align='center')
        drawLabel(f'{app.startingSun}', 60, 85, size=14, fill = 'black')
        # start game
        drawRect(880, 550, 100, 40, fill='darkRed', border='black', borderWidth=2)
        drawLabel('START', 930, 570, size=15, fill='cornSilk')
        drawLabel(f'Press "B" to return to the title screen!', 500, 570, size=15, fill='darkRed')
    elif app.onBackground == True:
        drawImage(app.bgImage, 0, 0, width=app.bgImageWidth, height=app.bgImageHeight)
        drawImage(app.zombieImg, 970, 120, width=app.zombWidth, height=app.zombHeight)
        drawLabel(f'Wave {app.wave}', 500, 570, size=15, fill='darkRed')
        # shelf
        drawRect(0, 0, 120, 400, fill='sienna',  border='black', borderWidth=2)
        drawLine(2, 110, 118, 110, fill='saddleBrown', lineWidth=2)
        drawCircle(60, 40, 30, fill='peru', border='saddleBrown', borderWidth=2)
        drawImage(app.sunImg, 60, 40, width=app.sun.sunWidth, height=app.sun.sunHeight, align='center')
        drawRect(60, 85, 70, 20, fill='blanchedAlmond', border='black', borderWidth=1, align='center')
        drawLabel(f'{app.startingSun}', 60, 85, size=14, fill = 'black')
        # menu
        drawRect(880, 550, 100, 40, fill='sienna', border='black', borderWidth=2)
        drawLabel('Menu', 930, 570, size=15, fill='cornSilk')
        # sun
        if app.timeUntilSun == 0:
            randomX = randrange(240,950)
            sunNew = Sun(75,randomX, 40)
            app.sunList.append(sunNew)
        for sun in range(len(app.sunList)):
            drawImage(app.sunImg, app.sunList[sun].sunSpawnX, app.sun.sunSpawnY, width=app.sun.sunWidth, height=app.sun.sunHeight, align='center')

    if app.onMenu == True:
        drawRect(app.cx, app.cy, 400, 200, fill='peru', border='black', borderWidth=1, align='center')
        drawRect(app.cx, 250, 250, 70, fill='peru', border='saddleBrown', borderWidth=1, align='center')
        drawRect(app.cx, 350, 250, 70, fill='peru', border='saddleBrown', borderWidth=1, align='center')
        drawLabel('Title Screen', 500, 250, size=15, fill='cornSilk', align='center')
        drawLabel('Restart', 500, 350, size=15, fill='cornSilk', align='center')
    

def onMousePress(app, mouseX, mouseY):
    print(mouseX)
    print(mouseY)
    # start game
    if mouseX > 178 and mouseX < 806 and mouseY > 504 and mouseY < 590:
        app.onTitle = False
        app.gameStart = True
        gameStart(app)
    # start gameplay
    elif app.gameStart == True and 880<mouseX<980 and 550<mouseY<590:
        app.gameStart = False
        app.onBackground = True
    # menu
    elif app.onBackground == True and 880<mouseX<980 and 550<mouseY<590:
        app.onMenu = True
    # return to title
    elif app.onMenu == True and 375<mouseX<625 and 215<mouseY<285:
        app.onMenu = False
        app.onBackground = False
        app.onTitle = True
    # restart
    elif app.onMenu == True and 375<mouseX<625 and 315<mouseY<385:
        app.onMenu = False
        app.wave = 1
        app.startingSun = 75
        app.sunList = []
    elif app.onMenu == True and mouseX<300 or mouseX>700 or mouseY<200 or mouseY>400:
        app.onMenu = False
    #if app.onBackground == True:

def onKeyPress(app, key):
    if key == 'd':
        app.onTitle = False
        app.directions = True
    elif app.directions == True and key == 'b':
        app.onTitle = True
        app.directions = False
    elif app.gameStart == True and key == 'b':
        app.onTitle = True

runApp()