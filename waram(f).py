# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, pygame, sys
from pygame.locals import *

FPS = 8   # Earthworm speed control
name = [] #Doo
GSCORE = []
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)



#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK


#Input Key Data
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # syntactic sugar: index of the worm's head

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Wormy')

    showStartScreen() # Functions that show the game screen

    Lv = showLevelSelectScreen() #Add difficulty setting

    while True:
        score = runGame(Lv)
        showGameOverScreen(score)

def runGame(Lv):
    addSpeed = 0
    # Set a random start point.
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    wormCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT

    # Start the apple in a random place.
    apple = getRandomLocation()

    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        # check if the worm has hit itself or the edge
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
            return score# game over
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return score# game over

        # check if worm has eaten an apply
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            # don't remove worm's tail segment
            apple = getRandomLocation() # set a new apple somewhere
        else:
            del wormCoords[-1] # remove worm's tail segment

        # move the worm by adding a segment in the direction it is moving
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}
        wormCoords.insert(0, newHead)
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords)
        drawApple(apple)
        score = len(wormCoords) - 3            
        addLevel = Lv
        addLevel = addLevel + (1 * (score//3)) # Increase by 1 level each time you eat 3
        addSpeed = 3 * addLevel                # The speed is increased by 3 every time the level is increased.
        drawScore(score, addLevel, (FPS+addSpeed))
        pygame.display.update()
        FPSCLOCK.tick(FPS+addSpeed)

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Wormy!', True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render('Wormy!', True, GREEN)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(15)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def showGameOverScreen(score):
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            name = []
            myName = showInputNameScreen() #Get player's initials

            saveNameAndScore(myName, score)
            printResult()
            return

def drawScore(score, level, speed):
    scoreSurf = BASICFONT.render('Score: %s / Level: %s / Speed: %s' % (score, level, speed), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 520, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)


def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))

def showLevelSelectScreen():
    myFont1 = pygame.font.Font('freesansbold.ttf', 30)
    myFont2 = pygame.font.Font('freesansbold.ttf', 20)
    
    LevelSurf1 = myFont1.render('= Select Level =', True, WHITE, DARKGREEN)
    LevelSurf2 = myFont2.render('1 2 3 4 5 6 7 8 9', True, GREEN)

    #Text box
    LevelSurfRect1 = LevelSurf1.get_rect()

    #Center point of the text box
    LevelSurfRect1.center = (320, 250)

    #Text box
    LevelSurfRect2 = LevelSurf2.get_rect()

    #Center point of the text box
    LevelSurfRect2.center = (320, 300)
    
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        DISPLAYSURF.blit(LevelSurf1, LevelSurfRect1)
        DISPLAYSURF.blit(LevelSurf2, LevelSurfRect2)

        #The part that sets the game's latitude(1~9)
        drawLevelSelectMsg()
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYUP:
                if(event.key == K_1):
                    return 1
            if event.type == KEYUP:
                if(event.key == K_2):
                    return 2
            if event.type == KEYUP:
                if(event.key == K_3):
                    return 3
            if event.type == KEYUP:
                if(event.key == K_4):
                    return 4
            if event.type == KEYUP:
                if(event.key == K_5):
                    return 5
            if event.type == KEYUP:
                if(event.key == K_6):
                    return 6
            if event.type == KEYUP:
                if(event.key == K_7):
                    return 7
            if event.type == KEYUP:
                if(event.key == K_8):
                    return 8
            if event.type == KEYUP:
                if(event.key == K_9):
                    return 9
            
            if event.type == KEYUP:
                if(event.key == 98):
                    return chr(event.key)
                
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawLevelSelectMsg():
    pressKeySurf = BASICFONT.render('Select Level (1 - 9) to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 450, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

def showInputNameScreen():
    myFont1 = pygame.font.Font('freesansbold.ttf', 30)
    myFont2 = pygame.font.Font('freesansbold.ttf', 20)
    
    LevelSurf1 = myFont1.render('= Enter Name =', True, WHITE, DARKGREEN)
    LevelSurf2 = myFont2.render('A B C D E F G H I J K L M N O P Q R S T U V W X Y Z', True, GREEN)

    #텍스트 박스
    LevelSurfRect1 = LevelSurf1.get_rect()
    #텍스트 박스의 중심점
    LevelSurfRect1.center = (320, 250)

    #텍스트 박스
    LevelSurfRect2 = LevelSurf2.get_rect()
    #텍스트 박스의 중심점
    LevelSurfRect2.center = (320, 300)
    
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        DISPLAYSURF.blit(LevelSurf1, LevelSurfRect1)
        DISPLAYSURF.blit(LevelSurf2, LevelSurfRect2)

        drawInputNameMsg()
        cnt = 0
        
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYUP:
                if(event.key >= 97 and event.key <= 122):
                    name.append(chr(event.key).upper())
                if(len(name)%3 == 0):
                    return name
      
        pygame.display.update()
        FPSCLOCK.tick(FPS)

#파일쓰기
def saveNameAndScore(name, score):
    #1
    f1 = open("name.txt",'a+') 
    f2 = open("score.txt",'a+')  
    strName=''.join(name)
    strScore=str(score)
    data = strName + '\n'
    print(data)
    f1.write(data)
    del name[2]
    del name[1]
    del name[0]
    data = strScore + ' '
    f2.write(data)

    f1.close() 
    f2.close()

def drawInputNameMsg():
    pressKeySurf = BASICFONT.render('Enter Your Initial. Press alphabet(A-Z).', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 450, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

def printResult():
    f = open('score.txt','r')
    lines = ' '
    lines = f.readlines() 

    #Values ​​read from the file are stored as a string
    for line in lines:
        print(line)

    list = line.split()       # The part that turns a string into a list 
    list.sort(reverse=True)   # Function to change list in descending order
    del list[10:] # I cut the part after the 10th of the list and do not use this part.


    scosco = ' '.join(list)   # Replaces list with string

    
    myFont1 = pygame.font.Font('freesansbold.ttf', 30)
    myFont2 = pygame.font.Font('freesansbold.ttf', 20)
    
    
    LevelSurf1 = myFont1.render('= Result =', True, WHITE, DARKGREEN)
    LevelSurf2 = myFont2.render('%s' % (scosco), True, GREEN)


    LevelSurfRect1 = LevelSurf1.get_rect()
    LevelSurfRect1.center = (320, 30)
    LevelSurfRect2 = LevelSurf2.get_rect()
    LevelSurfRect2.center = (320, 80)
    
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        DISPLAYSURF.blit(LevelSurf1, LevelSurfRect1) 
        DISPLAYSURF.blit(LevelSurf2, LevelSurfRect2)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYUP:
                return
      
        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__ == '__main__':
    main()
