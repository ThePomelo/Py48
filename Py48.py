import pygame, sys, random
from pygame.locals import *

boardwidth = 4
boardheight = 4
tilesize = 80
windowwidth = 640
windowheight = 480
fps = 60

controls = [K_UP,K_DOWN,K_LEFT,K_RIGHT,K_ESCAPE,K_TAB]

WHITE =         (250,250,250)
RED =           (250,  0,  0)
ORANGE =        (250,150,  0)
LIGHT_GREY =    (200,200,200)
GREY =          (175,175,175)
DARK_GREY =     (150,150,150)

colors = {
    0:(230,230,230),
    2:(238,228,218),
    4:(237,224,200),
    8:(242,171, 121),
    16:(245,149, 99),
    32:(246,124, 95),
    64:(246, 94, 59),
    128:(237,207,114),
    256:(237,204, 97),
    512:(237,200, 80),
    1024:(237,197, 63),
    2048:(250,210,  0)}

background_color = GREY
text_color = WHITE
num_size = 25
font_size = 20

xmargin = int((windowwidth - (tilesize*boardwidth + (boardwidth - 1)))/2)
ymargin = int((windowheight - (tilesize*boardheight + (boardheight - 1)))/2)


class Tile:
    def __init__(self, value, x, y, color = RED):
        self.value = value
        self.x = x
        self.y = y
        self.color = color
        
    def tile_color(self):
        self.color = colors[self.value]
        return self.color
        
    def combo(self):
        possible = False
        for (i,j) in [(0,-1),(1,0),(0,1),(-1,0)]:
            if self.x + i >= 0 and self.x + i <= boardwidth - 1 and self.y + j >= 0 and self.y + j <= boardheight - 1:
                if board[self.x + i][self.y + j].value == self.value:
                    possible = True
        return possible
        
    def num_color(self):
        if self.value < 8:
            color_num = DARK_GREY
        else:
            color_num = WHITE
        return color_num
            

def new_number():
    choices = []
    for y in range(boardheight):
        for x in range(boardwidth):
            if board[x][y].value == 0:
                choices.append(board[x][y])
    if len(choices) > 0:
        new_num = random.choice(choices)
        if turn < 20:
            new_num.value = 2
        else:
            prob = random.random()*100
            if prob < 90:
                new_num.value = 2
            else:
                new_num.value = 4
        
def wait():
    while True:
	fpsclock.tick(fps)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key in controls:
                return event.key

def move(key):
    score_bonus = 0
    turn_increase = 0
    
    if key == K_UP or key == K_DOWN:
        for x in range(boardwidth):            
            if key == K_UP:
                column = [board[x][y].value for y in range(boardheight)]
            elif key == K_DOWN:
                column = [board[x][y].value for y in range(boardheight)[::-1]]
            for k in range(1,boardheight):
                if 0 in column[0:k] and column[k] != 0:
                    turn_increase = 1
            for k in range(boardheight)[::-1]:
                if column[k] == 0: 
                    blank = column.pop(k)
                    column.append(blank)
            for k in range(boardheight - 1):
                if column[k] == column[k+1] and column[k] != 0:
                    turn_increase = 1
                    column[k] += column[k+1]
                    score_bonus += column[k]
                    column[k+1] -= column[k+1]
                    turn_increase = 1
            for k in range(len(column)):
                if column[k] == 0: 
                    blank = column.pop(k)
                    column.append(blank)
            for k in range(boardheight):
                if key == K_UP: board[x][k].value = column[k]
                elif key == K_DOWN: board[x][k].value = column[boardheight - 1 -k]
        
    elif key == K_LEFT or key == K_RIGHT:
        for y in range(boardheight):            
            if key == K_LEFT:
                row = [board[x][y].value for x in range(boardwidth)]
            elif key == K_RIGHT:
                row = [board[x][y].value for x in range(boardwidth)[::-1]]
            for k in range(1,boardwidth):
                if 0 in row[0:k] and row[k] != 0:
                    turn_increase = 1
            for k in range(boardwidth)[::-1]:
                if row[k] == 0: 
                    blank = row.pop(k)
                    row.append(blank)
            for k in range(boardwidth - 1):
                if row[k] == row[k+1] and row[k] != 0:
                    turn_increase = 1
                    row[k] += row[k+1]
                    score_bonus += row[k]
                    row[k+1] -= row[k+1]
                    turn_increase = 1
            for k in range(len(row)):
                if row[k] == 0: 
                    blank = row.pop(k)
                    row.append(blank)
            for k in range(boardwidth):
                if key == K_LEFT: board[k][y].value = row[k]
                elif key == K_RIGHT: board[k][y].value = row[boardheight - 1 -k]        
                        
    return (score_bonus,turn_increase)
            
def check_gameover():
    is_game_over = True
    for x in range(boardwidth):
        for y in range(boardheight):
            if board[x][y].combo() or board[x][y].value == 0:
                is_game_over = False
    return is_game_over
          
def check_2048():
    win = False
    for x in range(boardwidth):
        for y in range(boardheight):
            if board[x][y].value == 2048:
                win = True
    return win
    
def render_gameover():
    textsurf = basicfont.render('GAME OVER', True, WHITE, GREY)
    textrect = textsurf.get_rect()
    textrect.center = int(windowwidth / 2), int(windowheight - 40)
    displaysurf.blit(textsurf, textrect)
    closegame = wait()
    if closegame == K_ESCAPE:
        pygame.quit()
        sys.exit()
        
def render_winscreen():
    textsurf = basicfont.render('YOU WIN!', True, (250,250,0), GREY)
    textrect = textsurf.get_rect()
    textrect.center = int(windowwidth / 2), int(windowheight - 40)
    displaysurf.blit(textsurf, textrect)
    closegame = wait()
    if closegame == K_ESCAPE:
        pygame.quit()
        sys.exit() 

def render_tiles():
    for y in range(boardheight):
        for x in range(boardwidth):
            pygame.draw.rect(displaysurf, board[x][y].tile_color(), (xmargin + (tilesize + 5)*x, ymargin + (tilesize + 5)*y, tilesize, tilesize))
            if board[x][y].value != 0:
                textsurf = numfont.render(str(board[x][y].value),True,board[x][y].num_color())
                textrect = textsurf.get_rect()
                textrect.center = xmargin + (tilesize + 5)*x + int(tilesize/2),ymargin + (tilesize + 5)*y + int(tilesize/2)
                displaysurf.blit(textsurf, textrect)

def render_ui(disable_moves,disable_cycle,cycle_num):    
    textsurf = basicfont.render('Score: '+str(score), True, WHITE, GREY)
    textrect = textsurf.get_rect()
    textrect.center = int(windowwidth / 2), 40
    displaysurf.blit(textsurf, textrect)
    
    if not disable_moves:
        textsurf = basicfont.render('Moves: '+str(turn), True, WHITE, GREY)
        textrect = textsurf.get_rect()
        textrect.center = int(windowwidth / 2), int(windowheight - 40)
        displaysurf.blit(textsurf, textrect)
        
    if not disable_cycle:
        textsurf = basicfont.render(str(cycle_num), True, WHITE, GREY)
        textrect = textsurf.get_rect()
        textrect.topleft = 5,5
        displaysurf.blit(textsurf, textrect)
        
def handle_input(score_arg,turn_arg):
    turn_up = 0
    keypressed = wait()
    
    for event in pygame.event.get(QUIT): # get all the QUIT events
        pygame.quit()
        sys.exit() # terminate if any QUIT events are present

    if keypressed == K_ESCAPE:
        pygame.quit()
        sys.exit()
    elif keypressed in controls[0:4]:
        (bonus,turn_up) = move(keypressed)
        score_arg += bonus
    elif keypressed == K_TAB:
        board[0][0].value = 2048
    turn_arg += turn_up
    
    return (score_arg,turn_arg,bool(turn_up))
        
def initialize():
    global fpsclock,displaysurf,basicfont,numfont,background
    
    pygame.init()
    fpsclock = pygame.time.Clock()
    displaysurf = pygame.display.set_mode((windowwidth, windowheight))
    pygame.display.set_caption('Py48')
    basicfont = pygame.font.Font('freesansbold.ttf', font_size)
    numfont = pygame.font.Font('freesansbold.ttf', num_size)

    background = pygame.Surface(displaysurf.get_size())
    background = background.convert()
        
def make_board(display_all_nums = False):       
    global board
    
    board = [[Tile(0,x,y)
        for y in range(boardheight) ]
            for x in range(boardwidth) ]

    (x,y) = (random.choice(range(boardwidth)),random.choice(range(boardheight)))
    board[x][y].value = 2

    if display_all_nums:
        board[0][0].value = 2048
        board[1][0].value = 1024
        board[2][0].value = 512
        board[3][0].value = 256
        board[3][1].value = 128
        board[2][1].value = 64
        board[1][1].value = 32
        board[0][1].value = 16
        board[0][2].value = 8
        board[1][2].value = 4
        board[2][2].value = 2
        
def start_screen():
    global state
    while state == 0:
	fpsclock.tick(fps)
        background.fill(background_color)
        displaysurf.blit(background, (0,0))
        
        textsurf = basicfont.render('PY48: Press an arrow key to play.', True, WHITE, GREY)
        textrect = textsurf.get_rect()
        textrect.center = int(windowwidth / 2), int(windowheight / 2)
        displaysurf.blit(textsurf, textrect)
        pygame.display.update()
        
        start = wait()
        if start == K_ESCAPE:
            pygame.quit()
            sys.exit()
        elif start in controls[0:4]:
            state = 1 


make_board()
initialize()
    
turn = 0
score = 0
gameover = False
state = 0
cycle = 0
 
start_screen()            

while True:
    # Main game loop
    background.fill(background_color)
    displaysurf.blit(background, (0,0))
    
    render_ui(gameover,False,cycle)
    cycle += 1
    
    render_tiles()
    
    if gameover:
        if state == 1:
            render_gameover()
        elif state == 2:
            render_winscreen()

    if check_2048():
        state = 2
        gameover = True
    
    if not gameover:
        gameover = check_gameover()

    # DO ALL THE ANIMATION SHIT!!!
    
	fpsclock.tick(fps)
    
    
    pygame.display.update()
        
    if not gameover:
        (score,turn,turn_taken) = handle_input(score,turn)
        if turn_taken:
            new_number()
    
    
