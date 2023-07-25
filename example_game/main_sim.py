import numbers
import random, time, sys, os
from queue import Queue

# If Pi = False the script runs in simulation mode using pygame lib
import pygame
from pygame.locals import *

# only modify this two values for size adaption!
PIXEL_X=84  
PIXEL_Y=20

SIZE= 20
FPS = 15
BOXSIZE = 20
WINDOWWIDTH = BOXSIZE * PIXEL_X
WINDOWHEIGHT = BOXSIZE * PIXEL_Y
BOARDWIDTH = PIXEL_X
BOARDHEIGHT = PIXEL_Y
BLANK = '.'
LED_BRIGHTNESS = 0.6

#               R    G    B
WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
RED         = (255,   0,   0)
LIGHTRED    = (175,  20,  20)
GREEN       = (  0, 255,   0)
LIGHTGREEN  = ( 20, 175,  20)
BLUE        = (  0,   0, 255)
LIGHTBLUE   = ( 20,  20, 175)
YELLOW      = (255, 255,   0)
LIGHTYELLOW = (175, 175,  20)
CYAN        = (  0, 255, 255)
LIGHTCYAN   = ( 20, 175, 175)
MAGENTA     = (255,   0, 255)
LIGHTMAGENTA= (175,  20, 175)
ORANGE      = (255,  70,  10)
LIGHTORANGE = (175,  70,  10)
WHITE      = (255, 255, 255)
LIGHTWHITE = (175, 175, 175)

SCORES =(0,40,100,300,1200)

BORDERCOLOR = BLUE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY
COLORS      = (BLUE,GREEN,RED,YELLOW,CYAN,MAGENTA,ORANGE,WHITE)
LIGHTCOLORS = (LIGHTBLUE, LIGHTGREEN, LIGHTRED, LIGHTYELLOW, LIGHTCYAN,LIGHTMAGENTA, LIGHTORANGE,LIGHTWHITE)

TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5

# snake constants #
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # index of the worm's head

QKEYDOWN=0
QKEYUP=1

JKEY_X=0
JKEY_Y=3
JKEY_A=1
JKEY_B=2
JKEY_R=7
JKEY_L=6
JKEY_SEL=10
JKEY_START=11

mask = bytearray([1,2,4,8,16,32,64,128])
piece_counter = -1
piece_list = []
segment_mapping = [2,1,0,3] #colores for players

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT
    global a1_counter ,RUNNING
    a1_counter=0
    RUNNING=True
    joystick_detected=False
    joystick_cnt=0
    
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((PIXEL_X*SIZE, PIXEL_Y*SIZE))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
    pygame.display.set_caption('Pi Games')
    DISPLAYSURF.fill(BGCOLOR)
    pygame.joystick.init()
    joystick_count = pygame.joystick.get_count()
    joystick=[]
    for i in range(joystick_count):
        joystick.append(pygame.joystick.Joystick(i))
        joystick[i].init()

    pygame.display.update()
    pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP,JOYBUTTONDOWN,JOYAXISMOTION])
    time.sleep(2)
   
    while True:
        clearScreen()
        updateScreen()
        checkForQuit()
        
        runSnakeGame()
        time.sleep(.1)
    terminate()

# gaming main routines #

class snake:
    # Set a random start point.
    startx = 0
    starty = 0
    wormCoords = []
    direction = RIGHT
    olddirection =0
    score = 0
    apple=[]
    
    def __init__(self): 
        self.startx = random.randint(2, BOARDWIDTH-2 )
        self.starty = random.randint(2, BOARDHEIGHT -2 )
        self.wormCoords = [  {'x': self.startx,     'y': self.starty},
                        {'x': self.startx - 1, 'y': self.starty},
                        {'x': self.startx - 2, 'y': self.starty}]
        self.apple = self.getRandomLocation()
    # Start the apple in a random place.
    
    def getRandomLocation(self):
        while True:
            x = random.randint(0, BOARDWIDTH - 1)
            y = random.randint(0, BOARDHEIGHT - 1)
            if {'x': x, 'y': y} in self.wormCoords:
                print('no apples on worm')
            else:
                break
        return {'x': x, 'y': y}
   
def runSnakeGame():
    print("snake started")
    players = 4
    snakes = []
    tBoards = []
     # define keys for 4 players
    keylist = []
    joystick_mapping = [2,3,1,0]
    keylist.append([K_LEFT,K_RIGHT,K_DOWN,K_UP,K_3,K_4])
    keylist.append([K_a,K_d,K_s,K_w,K_q,K_e])
    keylist.append([K_f,K_h,K_g,K_t,K_r,K_z])
    keylist.append([K_j,K_l,K_k,K_i,K_u,K_o])

    for i in range(0,players):
        snakes.append(snake())

    while True: # main game loop
        
        for s_i in range(0,players):
            snakes[s_i].olddirection = snakes[s_i].direction
            pygame.event.pump()
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    jid = event.joy
                    j = joystick_mapping[jid]
                    axis = event.axis
                    val = round(event.value)
                    if (snakes[j].olddirection== snakes[j].direction):  
                        if (axis == 0 and val == -1):
                            if snakes[j].direction != RIGHT:
                                snakes[j].direction = LEFT
                        if (axis == 0 and val == 1):
                            if snakes[j].direction != LEFT:
                                snakes[j].direction = RIGHT
                        if (axis == 1 and val == 1):
                            if snakes[j].direction != UP:
                                snakes[j].direction = DOWN
                        if (axis == 1 and val == -1):
                            if snakes[j].direction != DOWN:
                                snakes[j].direction = UP

                if event.type == pygame.KEYDOWN:
                    klist_index = 0
                    for kl in keylist:
                        if event.key in kl:
                            break
                        klist_index=klist_index+1
                    if klist_index<players:
                        if (event.key==keylist[klist_index][0]):
                            if snakes[klist_index].direction != RIGHT:
                                snakes[klist_index].direction = LEFT
                        if (event.key==keylist[klist_index][1]):
                            if snakes[klist_index].direction != LEFT:
                                snakes[klist_index].direction = RIGHT
                        if (event.key==keylist[klist_index][2]):
                            if snakes[klist_index].direction != UP:
                                snakes[klist_index].direction = DOWN
                        if (event.key==keylist[klist_index][3]):
                            if snakes[klist_index].direction != DOWN:
                                snakes[klist_index].direction = UP

            # check if the worm has hit itself or the edge
            if snakes[s_i].wormCoords[HEAD]['x'] == -1 or snakes[s_i].wormCoords[HEAD]['x'] == BOARDWIDTH or snakes[s_i].wormCoords[HEAD]['y'] == -1 or snakes[s_i].wormCoords[HEAD]['y'] == BOARDHEIGHT:
                time.sleep(1.5)
                return # game over
            for wormBody in snakes[s_i].wormCoords[1:]:
                if wormBody['x'] == snakes[s_i].wormCoords[HEAD]['x'] and wormBody['y'] == snakes[s_i].wormCoords[HEAD]['y']:
                    time.sleep(1.5)
                    return # game over

            # check if worm has eaten an apple
            if snakes[s_i].wormCoords[HEAD]['x'] == snakes[s_i].apple['x'] and snakes[s_i].wormCoords[HEAD]['y'] == snakes[s_i].apple['y']:
                # don't remove worm's tail segment
                snakes[s_i].score += 1
                snakes[s_i].apple = snakes[s_i].getRandomLocation() # set a new apple somewhere
            else:
                del snakes[s_i].wormCoords[-1] # remove worm's tail segment

            # move the worm by adding a segment in the direction it is moving
            if snakes[s_i].direction == UP:
                if snakes[s_i].wormCoords[HEAD]['y'] == 0 :
                    newHead = {'x': snakes[s_i].wormCoords[HEAD]['x'], 'y': BOARDHEIGHT-1}
                else:
                    newHead = {'x': snakes[s_i].wormCoords[HEAD]['x'], 'y': snakes[s_i].wormCoords[HEAD]['y'] - 1}
            elif snakes[s_i].direction == DOWN:
                if snakes[s_i].wormCoords[HEAD]['y'] == BOARDHEIGHT-1 :
                    newHead = {'x': snakes[s_i].wormCoords[HEAD]['x'], 'y': 0}
                else:
                    newHead = {'x': snakes[s_i].wormCoords[HEAD]['x'], 'y': snakes[s_i].wormCoords[HEAD]['y'] + 1}
            elif snakes[s_i].direction == LEFT:
                if snakes[s_i].wormCoords[HEAD]['x'] == 0 :
                    newHead = {'x': BOARDWIDTH -1, 'y': snakes[s_i].wormCoords[HEAD]['y'] }
                else:
                    newHead = {'x': snakes[s_i].wormCoords[HEAD]['x'] - 1, 'y': snakes[s_i].wormCoords[HEAD]['y']}
            elif snakes[s_i].direction == RIGHT:
                if snakes[s_i].wormCoords[HEAD]['x'] == BOARDWIDTH-1:
                    newHead = {'x': 0, 'y': snakes[s_i].wormCoords[HEAD]['y']}
                else:
                    newHead = {'x': snakes[s_i].wormCoords[HEAD]['x'] + 1, 'y': snakes[s_i].wormCoords[HEAD]['y']}
        
            snakes[s_i].wormCoords.insert(0, newHead)
        checkForQuit()
        clearScreen()

        for i in range(0,players):
            drawWorm(snakes[i].wormCoords,2*i)
            drawApple(snakes[i].apple,2*i+1)
        updateScreen()
        time.sleep(.15)
        

def drawWorm(wormCoords,color):
    for coord in wormCoords:
        x = coord['x']
        y = coord['y']
        drawPixel(x,y,color)

def drawApple(coord, color):
    x = coord['x']
    y = coord['y']
    drawPixel(x,y,color)

def clearScreen():
    DISPLAYSURF.fill(BGCOLOR)

def updateScreen():
    pygame.display.update()


#### do not modify this section !!!

def drawPixel(x,y,color):
    if color == BLANK:
        return
    pygame.draw.rect(DISPLAYSURF, COLORS[color], (x*SIZE+1, y*SIZE+1, SIZE-2, SIZE-2))

def drawLightPixel(x,y,color):
    if color == BLANK:
        return
    pygame.draw.rect(DISPLAYSURF, LIGHTCOLORS[color], (x*SIZE+1, y*SIZE+1, SIZE-2, SIZE-2))

def drawPixelRgb(x,y,r,g,b):
    pygame.draw.rect(DISPLAYSURF, (r,g,b), (x*SIZE+1, y*SIZE+1, SIZE-2, SIZE-2))

def terminate():
    RUNNING = False
    pygame.quit()
    exit()

def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back

def drawBoard(matrix,offset):
    for i in range(offset,offset+10):
        for j in range(0,BOARDHEIGHT):
            drawPixel(i,j,matrix[i-offset][j])

if __name__ == '__main__':
    main()
