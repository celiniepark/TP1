from cmu_graphics import *
import math, copy
from PIL import Image
import os, pathlib
import random
# cmugraphicsdemos: basicPILMethods.py, kirbleBirdStarter.py
# CS Academy: distance function, 5.3.4 Tic Tac Toe
# https://ernestoam.fandom.com/wiki/Category:Plants_vs._Zombies_2

class Sun:
    def __init__(self, x, y):
        self.sunWidth, self.sunHeight = 35, 35
        self.sunSpawnX = x
        self.sunSpawnY = y
    def sunFall(self, sunSpawnY):
        self.sunSpawnY += 10
    
class Seed:
    def __init__(self):
        self.width = 230 // 2.5
        self.height = 150 // 2.5

#zombie class   
class Zombie:
    def __init__(self, speed):
        self.speed = speed
        zombGif = Image.open('gifs/pvz_normZombie.gif')
        self.spriteList = []
        for frame in range(zombGif.n_frames): 
            zombGif.seek(frame)
            fr = zombGif.resize((zombGif.size[0]//2, zombGif.size[1]//2))
            fr = CMUImage(fr)
            self.spriteList.append(fr)
        self.stepCounter = 0
        self.spriteCounter = 0
        self.spriteList.pop(0)
    
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
    app.timeUntilSun = 30
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
    app.stepsPerSecond = 100

    # menu screen
    app.onMenu = False
    # -------seeds-------
    # sunflower
    app.sunflowerSeed = openImage('../sunflower_seed.png')
    app.sunflowerSeedImg = CMUImage(app.sunflowerSeed)
    app.sunflowerSeed = Seed()
    # peashooter
    app.peashooterSeed = openImage('../peashooter_seed.png')
    app.peashooterSeedImg = CMUImage(app.peashooterSeed)
    app.peashooterSeed = Seed()
    # wallnut
    app.wallnutSeed = openImage('../wallnut_seed.png')
    app.wallnutSeedImg = CMUImage(app.wallnutSeed)
    app.wallnutSeed = Seed()
    # -------zombie-------
    app.zombie = openImage('../normZomb.png')
    app.zombieImg = CMUImage(app.zombie)
    app.zombWidth, app.zombHeight = 70, 120
    app.zombie = Zombie(5)

    # -------sun-------
    app.sun = openImage('../pvz_sun.png')
    app.sunImg = CMUImage(app.sun)
    app.sun = Sun(0,40)
    app.startingSun = 75
    app.sunList = []

def distance(x1, y1, x2, y2):
    n = math.sqrt(abs((x1 - x2)**2 + (y1 - y2)**2))
    return n

def gameStart(app):
    app.gameStart = True
    app.wave = 1
    app.sunList = []
def openImage(fileName):
   return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))

def onStep(app):
    # sun spawn and fall
    if app.onBackground == True and app.timeUntilSun > 0:
        app.timeUntilSun -= 1
    elif app.timeUntilSun == 0:
        app.timeUntilSun = 30
    for sun in app.sunList:
        sun.sunSpawnY += 1
    if app.onBackground == True:
        app.zombie.stepCounter += 1
        if app.zombie.stepCounter >= 3:
            app.zombie.spriteCounter = (app.zombie.spriteCounter + 1) % len(app.zombie.spriteList)
            app.zombie.stepCounter = 0

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
        drawLabel("4. Use Wall-Nuts as a defensive shield!", 500, 250, size=20, fill='cornSilk')
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
        drawImage(app.zombie.spriteList[app.zombie.spriteCounter], 960, 120, width=app.zombWidth, height=app.zombHeight)
        drawLabel(f'Wave {app.wave}', 500, 570, size=15, fill='darkRed')
        # shelf
        drawRect(0, 0, 120, 400, fill='sienna',  border='black', borderWidth=2)
        drawLine(2, 110, 118, 110, fill='saddleBrown', lineWidth=2)
        drawCircle(60, 40, 30, fill='peru', border='saddleBrown', borderWidth=2)
        drawImage(app.sunImg, 60, 40, width=app.sun.sunWidth, height=app.sun.sunHeight, align='center')
        drawRect(60, 85, 70, 20, fill='blanchedAlmond', border='black', borderWidth=1, align='center')
        drawLabel(f'{app.startingSun}', 60, 85, size=14, fill = 'black')
        # seeds
        drawImage(app.sunflowerSeedImg, 60, 145, width=app.sunflowerSeed.width, height=app.sunflowerSeed.height, align = 'center')
        drawRect(60, 190, 70, 20, fill='blanchedAlmond', border='black', borderWidth=1, align='center')
        drawLabel('50', 60, 190, size=14, fill = 'black')
        drawImage(app.peashooterSeedImg, 60, 240, width=app.sunflowerSeed.width, height=app.sunflowerSeed.height, align = 'center')
        drawRect(60, 285, 70, 20, fill='blanchedAlmond', border='black', borderWidth=1, align='center')
        drawLabel('100', 60, 285, size=14, fill = 'black')
        drawImage(app.wallnutSeedImg, 60, 335, width=app.sunflowerSeed.width, height=app.sunflowerSeed.height, align = 'center')
        drawRect(60, 380, 70, 20, fill='blanchedAlmond', border='black', borderWidth=1, align='center')
        drawLabel('100', 60, 380, size=14, fill = 'black')
        # menu
        drawRect(880, 550, 100, 40, fill='sienna', border='black', borderWidth=2)
        drawLabel('Menu', 930, 570, size=15, fill='cornSilk')
        # sun
        if app.timeUntilSun == 0:
            randomX = randrange(240,950)
            sunNew = Sun(randomX, 40)
            app.sunList.append(sunNew)
        for sun in app.sunList:
            drawImage(app.sunImg, sun.sunSpawnX, sun.sunSpawnY, width=sun.sunWidth, height=sun.sunHeight, align='center')

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
    # pick up sun
    for sun in app.sunList:
        if distance(sun.sunSpawnX, sun.sunSpawnY, mouseX, mouseY) < 17.5:
            app.sunList.remove(sun)
            app.startingSun += 25

def onKeyPress(app, key):
    if key == 'd':
        app.onTitle = False
        app.directions = True
    elif app.directions == True and key == 'b':
        app.onTitle = True
        app.directions = False
    elif app.gameStart == True and key == 'b':
        app.onTitle = True

# def findSlot(app, mouseX, mouseY)
runApp()
