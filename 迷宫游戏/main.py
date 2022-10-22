from random import randint, choice
from enum import Enum
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'


class MAP_ENTRY_TYPE(Enum):
    MAP_EMPTY = 0,
    MAP_BLOCK = 1,

class WALL_DIRECTION(Enum):
    WALL_LEFT = 0,
    WALL_UP = 1,
    WALL_RIGHT = 2,
    WALL_DOWN = 3,

class Map():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = [[0 for x in range(self.width)] for y in range(self.height)]

    def resetMap(self, value):
        for y in range(self.height):
            for x in range(self.width):
                self.setMap(x, y, value)

    def setMap(self, x, y, value):
        if value == MAP_ENTRY_TYPE.MAP_EMPTY:
            self.map[y][x] = 0
        elif value == MAP_ENTRY_TYPE.MAP_BLOCK:
            self.map[y][x] = 1

    def isVisited(self, x, y):
        return self.map[y][x] != 1

    def showMap(self):
        for x in range(WIDTH):
            for y in range(HEIGHT):
                if self.map[x][y] == 1:
                    screen.blit(bar_small_list[decoration_list[x][y]], (y * WALL_WIDTH_SMALL + 530, x * WALL_WIDTH_SMALL + 30)) # 横着画一行，然后再换行

    def getMap(self):
        maze = []
        for row in self.map:
            row_list = []
            for entry in row:
                row_list.append(entry)
            maze.append(row_list)
        maze[HEIGHT-2][WIDTH-1] = 100
        return maze

# find unvisited adjacent entries of four possible entris
# then add random one of them to checklist and mark it as visited
def checkAdjacentPos(map, x, y, width, height, checklist):
    directions = []
    if x > 0:
        if not map.isVisited(2 * (x - 1) + 1, 2 * y + 1):
            directions.append(WALL_DIRECTION.WALL_LEFT)

    if y > 0:
        if not map.isVisited(2 * x + 1, 2 * (y - 1) + 1):
            directions.append(WALL_DIRECTION.WALL_UP)

    if x < width - 1:
        if not map.isVisited(2 * (x + 1) + 1, 2 * y + 1):
            directions.append(WALL_DIRECTION.WALL_RIGHT)

    if y < height - 1:
        if not map.isVisited(2 * x + 1, 2 * (y + 1) + 1):
            directions.append(WALL_DIRECTION.WALL_DOWN)

    if len(directions):
        direction = choice(directions)
        if direction == WALL_DIRECTION.WALL_LEFT:
            map.setMap(2 * (x - 1) + 1, 2 * y + 1, MAP_ENTRY_TYPE.MAP_EMPTY)
            map.setMap(2 * x, 2 * y + 1, MAP_ENTRY_TYPE.MAP_EMPTY)
            checklist.append((x - 1, y))
        elif direction == WALL_DIRECTION.WALL_UP:
            map.setMap(2 * x + 1, 2 * (y - 1) + 1, MAP_ENTRY_TYPE.MAP_EMPTY)
            map.setMap(2 * x + 1, 2 * y, MAP_ENTRY_TYPE.MAP_EMPTY)
            checklist.append((x, y - 1))
        elif direction == WALL_DIRECTION.WALL_RIGHT:
            map.setMap(2 * (x + 1) + 1, 2 * y + 1, MAP_ENTRY_TYPE.MAP_EMPTY)
            map.setMap(2 * x + 2, 2 * y + 1, MAP_ENTRY_TYPE.MAP_EMPTY)
            checklist.append((x + 1, y))
        elif direction == WALL_DIRECTION.WALL_DOWN:
            map.setMap(2 * x + 1, 2 * (y + 1) + 1, MAP_ENTRY_TYPE.MAP_EMPTY)
            map.setMap(2 * x + 1, 2 * y + 2, MAP_ENTRY_TYPE.MAP_EMPTY)
            checklist.append((x, y + 1))
        return True
    else:
        # if not find any unvisited adjacent entry
        return False


# random prim algorithm
def randomPrim(map, width, height):
    startX, startY = (randint(0, width - 1), randint(0, height - 1))
    map.setMap(2 * startX + 1, 2 * startY + 1, MAP_ENTRY_TYPE.MAP_EMPTY)

    checklist = []
    checklist.append((startX, startY))
    while len(checklist):
        # select a random entry from checklist
        entry = choice(checklist)
        if not checkAdjacentPos(map, entry[0], entry[1], width, height, checklist):
            # the entry has no unvisited adjacent entry, so remove it from checklist
            checklist.remove(entry)

def doRandomPrim(map):
    # set all entries of map to wall
    map.resetMap(MAP_ENTRY_TYPE.MAP_BLOCK)
    randomPrim(map, (map.width - 1) // 2, (map.height - 1) // 2)

#student_code_starts

import sys
import pygame # 导入 Pygame 库

WALL_WIDTH_BIG = 90
WALL_HEIGHT_BIG = 94
PLAYER_BIG = 100

WALL_WIDTH_SMALL = 16
WALL_HEIGHT_SMALL = 16
PLAYER_SMALL = 16

#小地图透明度
MAP_TRANSPOERT = 155

# 判断向上是否能走
def goUp(row, col):
    row_new = row - 1
    foot.play()
    if maze[row_new][col] == 1:
        colide.play()
        return [row, col]
    else:
        return [row_new, col]

# 判断向下是否能走
def goDown(row, col):
    row_new = row + 1
    foot.play()
    if maze[row_new][col] == 1:
        colide.play()
        return [row, col]
    else:

        return [row_new, col]

# 判断向左是否能走
def goLeft(row, col):
    col_new = col - 1
    foot.play()
    if maze[row][col_new] == 1:
        colide.play()
        return [row, col]
    else:
        return [row, col_new]

# 判断向右是否能走
def goRight(row, col):
    global status
    if row == 23 and col == 24:
        status = '胜利'
        return [row, col]
    col_new = col + 1
    foot.play()
    if maze[row][col_new] == 1:
        colide.play()
        return [row, col]
    else:
        return [row, col_new]

# 画小迷宫
def drawMap():
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if maze[i][j] == 1:
                screen.blit(bar_small_list[decoration_list[i][j]], (j * WALL_WIDTH_SMALL+100, i * WALL_WIDTH_SMALL+100)) # 横着画一行，然后再换行

# 画正常版全身小人
def drawPlayer(direction):
    global frame
    tag = frame // 10
    if direction == 'up':
        pic = up_list[tag]
    elif direction == 'down':
        pic = down_list[tag]
    elif direction == 'left':
        pic = left_list[tag]
    elif direction == 'right':
        pic = right_list[tag]
    screen.blit(pic, (260, 250))

    frame = frame + 1
    if frame >= 80:
        frame = 0

# 画大头
def drawHead():
    screen.blit(player_head, (position[1] * WALL_WIDTH_SMALL+100, position[0] * WALL_WIDTH_SMALL+100))


# 画局部迷宫
def drawMaze():
    min_row = position[0] - 3
    max_row = position[0] + 3
    min_col = position[1] - 3
    max_col = position[1] + 3
    for i in range(min_row+1, max_row):
        if i>=0 and i<HEIGHT:
            for j in range(min_col, max_col):
                if j>=0 and j<WIDTH:
                    if maze[i][j]==1:
                        screen.blit(bars[decoration_list[i][j]],((j-min_col) * WALL_WIDTH_BIG, (i-min_row) * WALL_WIDTH_BIG))  # 横着画一行，然后再换行

pygame.init() # 初始化
pygame.mixer.init() # 初始化音频
screen = pygame.display.set_mode((600,600)) #创建游戏窗口
FPS = 60
clock =pygame.time.Clock()

# 导入音频
pygame.mixer.music.load('music/背景音乐.mp3')
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)
colide = pygame.mixer.Sound('music/撞击.mp3')
colide.set_volume(0.6)
foot = pygame.mixer.Sound('music/脚步.mp3')
foot.set_volume(0.5)


# 加载背景
bg = pygame.image.load('pic/bg.png')
bg = pygame.transform.smoothscale(bg, (2900, 2900))
# 加载墙壁图片
bars = []
for i in range(2):
    bars.append(pygame.image.load(f'pic/bar_big{i}.png'))
    
bar_small_list = []
for i in range(2):
    bar_small_list.append(pygame.image.load(f'pic/bar_small{i}.png'))


# 加载角色大头图片
player_head = pygame.image.load('pic/player_small.png')


# 加载正常版角色全身图片
up_list = []
down_list = []
left_list = []
right_list = []
for i in range(8):
    up_name = f'pic/player/player_big/up/up ({i + 1}).png'
    down_name = f'pic/player/player_big/down/down ({i + 1}).png'
    left_name = f'pic/player/player_big/left/left ({i + 1}).png'
    right_name = f'pic/player/player_big/right/right ({i + 1}).png'
    up_list.append(pygame.image.load(up_name))
    down_list.append(pygame.image.load(down_name))
    left_list.append(pygame.image.load(left_name))
    right_list.append(pygame.image.load(right_name))


# 迷雾遮罩
map_mask = pygame.image.load('pic/暗角.png')
map_mask = pygame.transform.smoothscale(map_mask,(600,600))

# 胜利
win = pygame.image.load('pic/win.png')

# 初始化倒计时
font = pygame.font.Font(None, 100)
counter = 99
text = font.render(str(counter), True, 'gold')
timer_event = pygame.USEREVENT+1
pygame.time.set_timer(timer_event, 1000)


# 初始化迷宫
WIDTH = 25
HEIGHT = 25
map = Map(WIDTH, HEIGHT)
doRandomPrim(map)
maze = map.getMap()

# 预设墙壁的图案
decoration_list = []
for x in range(HEIGHT):
    row_list = []
    for y in range(WIDTH):
        row_list.append(randint(0, 1))
    decoration_list.append(row_list)

direction = 'down'
frame = 0
position = [1, 1]
map_status = 0
status = '游戏中'

# 主循环模块
while True:
    # 遍历事件队列
    for event in pygame.event.get():
        if event.type == pygame.QUIT or counter == 0: # 点击右上角的'X'，终止主循环
            sys.exit()
        if status == '游戏中':
            if event.type == pygame.KEYDOWN:
                if map_status == 0:
                    if event.key == pygame.K_UP:
                        direction = 'up'
                        position = goUp(position[0], position[1])
                    if event.key == pygame.K_DOWN:
                        direction = 'down'
                        position = goDown(position[0], position[1])
                    if event.key == pygame.K_LEFT:
                        direction = 'left'
                        position = goLeft(position[0], position[1])
                    if event.key == pygame.K_RIGHT:
                        direction = 'right'
                        position = goRight(position[0], position[1])
                if event.key == pygame.K_SPACE:
                        map_status = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    map_status = 0
               
            # 判断倒计时功能
            if event.type == timer_event:
                counter = counter - 1
                text = font.render(str(counter), True, 'gold')
                if counter == 0:
                    pygame.time.set_timer(timer_event, 0)

    screen.blit(bg, ((position[1]-1)*-100,(position[0]-1)*-100))

    # 画局部迷宫
    drawMaze()
    # 画正常版全身小人
    drawPlayer(direction)
     # 画遮罩
    screen.blit(map_mask, (0, 0))
    if map_status == 1:
        # 画地图遮罩
        screen.blit(map_mask, (100, 100))
        # 画完整迷宫
        drawMap()
        # 画角色大头
        drawHead()
        
    
        
    # 画倒计时
    screen.blit(text, (500, 0))

    if status == '胜利':
        screen.blit(win, (150, 150))
    pygame.display.update() # 重绘界面
    clock.tick(FPS)

# student_code_ends