from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'  
#student_code_starts
from function import *
import pygame
import sys

# 初始化
pygame.init()  # pygame 初始化
pygame.mixer.init() # pygame 音频初始化
screen = pygame.display.set_mode((800, 600))  # 创建屏幕

# 加载图片
background = pygame.image.load('pic/背景.png')  # 加载背景图片
chessboard = pygame.image.load('pic/棋盘.png')  # 加载棋盘图片
black = pygame.image.load('pic/黑棋.png')  # 加载黑棋的图片
white = pygame.image.load('pic/白棋.png')  # 加载白棋的图片
chessboard.set_alpha(255) # 可以尝试在这里设置棋盘透明度（0-255）

# 加载背景音乐
pygame.mixer.music.load('music/背景音乐.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1, 0) # 背景音乐一直重复

# 加载音效
drop_sound = pygame.mixer.Sound('music/落子.WAV')
drop_sound.set_volume(0.3)

# 初始化变量
game = '游戏中'  # 游戏状态 
# 初始化颜色状态机变量
status = 'black'


# 创建二维列表
gobang = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]  # 二维列表，用于储存游戏落子状态


# 主循环
while True:
    # 事件检测
    for event in pygame.event.get():
        # 退出游戏
        if event.type == pygame.QUIT:
            sys.exit()
        if game == '游戏中':
            # 鼠标点击事件
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 获取鼠标坐标
                pos= pygame.mouse.get_pos()
                x = pos[0]
                y = pos[1]
                if x  <= 600:
                    # 鼠标坐标转换成对应行、列号
                    row = y // 60 # 计算行号
                    col = x // 60 # 计算列号
                    if gobang[row][col] == 0:
                        # 改变棋子的颜色
                        # 落子为黑棋，改变列表值
                        if status == 'black':
                            gobang[row][col] = 1
                            status = 'white'
                        # 落子为白棋，改变列表值
                        elif status == 'white':
                            gobang[row][col] = 2
                            status = 'black'
                        # 播放落子音效
                        drop_sound.play()
        else:
            # 判断r键是否按下
            if event.type == pygame.KEYDOWN:
                if game != '游戏中' and event.key == pygame.K_r:
                    # 重置棋盘：将二位列表所有元素重新赋值为0
                    for row in range(10):
                        for col in range(10):
                            gobang[col][row] = 0
                    # 重置变量
                    game = '游戏中'
                    status = 'black'
                
    # 绘制背景
    screen.blit(background, (0, 0))
    # 绘制棋盘
    screen.blit(chessboard, (0, 0))

    # 双循环读取二位列表绘制棋子
    for row in range(10):
        for col in range(10):
            # 绘制黑棋棋子
            if gobang[row][col] == 1:
                screen.blit(black, (col * 60, row * 60))
            # 绘制白棋棋子
            elif gobang[row][col] == 2:
                screen.blit(white, (col * 60, row * 60))

    # 游戏中
    if game == '游戏中':
        # 检查游戏的状态
        game = check(screen, status, gobang)
    # 游戏结束
    else:
        # 显示游戏结果
        show_result(screen, game)
    # 切换鼠标的形态
    if status == 'black':
        mouse_chess(pygame.mouse.get_pos(),screen, black)
    else:
        mouse_chess(pygame.mouse.get_pos(),screen, white)
    


    # 更新屏幕
    pygame.display.update()


#student_code_ends
