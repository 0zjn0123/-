from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'  
score_list =[
    [0, 9, 90, 900, 9000, 90000],
    [0, 10, 100, 1000, 10000, 1000000],
]

direction_list = [[0, 1],  # 行
                  [1, 0],  # 列
                  [1, 1],  # 右下
                  [1, -1]  # 左下
                  ]


def aiChess():
    max_score = 0  # 最大分数
    row_new = 0
    col_new = 0
    for i in range(WIDTH):
        for j in range(HEIGHT):
            score = 0  # 改点位的分数
            for color in range(1, 3):

                if status == 'black':
                    other = 2
                else:
                    other = 1
                if gobang[i][j] == 0:
                    gobang[i][j] = color  # 假设在 i 行 j 列，放上 color 色的子

                    for x, y in direction_list:
                        max_combo = 0  # 最大的连续棋子数，并包含 i 行 j 列这个子

                        for k in range(-4, 1):
                            combo = 0  # 连续的棋子数
                            center = False  # 计数时是否包含 i 行 j 列这个子

                            # 横向
                            row = i + k * x
                            col = j + k * y

                            row = row - x  # 初始化，方便后面减1操作
                            col = col - y

                            # 先看左边是不是墙，或者另外颜色
                            if col<0 or col>= WIDTH or row<0 or row>HEIGHT:
                                side = 1
                            elif gobang[row][col] == other:
                                side = 1
                            else:
                                side = 0

                            for l in range(5):
                                # 横向
                                row = row + x
                                col = col + y
                                if 0 <= row < WIDTH and 0 <= col < WIDTH:  # 判断格子是否在边界外
                                    if gobang[row][col] == color:  # 判断该格子是否为当前颜色
                                        combo = combo + 1
                                        if row == i and col == j:
                                            center = True

                                    else:  # 如果格子是对方或者是空格
                                        if gobang[row][col] == other:
                                            side = side + 1  # 如果结束的是对方棋子，封边加1

                                        # 通用情况
                                        if (side == 2) and (combo != 5):
                                            combo = 0  # 如果两边都堵了,combo 归0
                                        elif (side == 1) and (combo != 5):
                                            combo = combo - 1  # 如果堵了一边，combo 相当于少了 1
                                        if center == True:  # 判断 i 行 j 列有没有在这个计算序列里
                                            if combo > max_combo:  # combo 数大于原本的时候
                                                max_combo = combo
                                        combo = 0
                                        center = False
                                        if gobang[row][col] == other:
                                            side = 1  # 如果结束的是对方棋子，下次封边是1
                                        else:
                                            side = 0 # 如果是空格，那就是0


                                else:  # 如果超边界
                                    side = side + 1  # 封边加1
                                    # 通用情况
                                    if (side == 2) and (combo != 5):
                                        combo = 0  # 如果两边都堵了,combo 归0
                                    elif (side == 1) and (combo != 5):
                                        combo = combo - 1  # 如果堵了一边，combo 相当于少了 1
                                    if center == True:  # 判断 i 行 j 列有没有在这个计算序列里
                                        if combo > max_combo:  # combo 数大于原本的时候
                                            max_combo = combo
                                    combo = 0
                                    center = False
                                    side = 1

                            # 五子判断结束后，再判断第六个是否为空格,并结尾处理
                            if 0 <= row + x < WIDTH and 0 <= col + y < WIDTH:  # 判断格子是否在边界内
                                if gobang[row + x][col + y] != 0:
                                    side = side + 1  # 如果结束的不是空格，封边加1
                            else:
                                side = side + 1
                            # 通用情况
                            if (side == 2) and (combo != 5):
                                combo = 0  # 如果两边都堵了,combo 归0
                            elif (side == 1) and (combo != 5):
                                combo = combo - 1  # 如果堵了一边，combo 相当于少了 1
                            if center == True:  # 判断 i 行 j 列有没有在这个计算序列里
                                if combo > max_combo:  # combo 数大于原本的时候
                                    max_combo = combo

                        score = score + score_list[color - 1][max_combo]
                    gobang[i][j] = 0
            if score > max_score:
                max_score = score
                row_new = i
                col_new = j

    return row_new, col_new


#student_code_starts
from function import *
import sys

WIDTH = 20
HEIGHT = 20



# 初始化
pygame.init()  # pygame 初始化
pygame.mixer.init() # pygame 音频初始化
screen = pygame.display.set_mode((1250, 700))  # 创建屏幕

# 加载图片
background = pygame.image.load('pic/背景.png') # 加载背景图片
chessboard = pygame.image.load('pic/棋盘2.png')  # 加载棋盘图片
black = pygame.image.load('pic/黑棋.png')  # 加载黑棋的图片
white = pygame.image.load('pic/白棋.png')  # 加载白棋的图片
button = pygame.image.load('pic/按钮.png') # 加载撤回按钮的图片
chessboard.set_alpha(255) # 可以尝试在这里设置棋盘透明度（0-255）

black = pygame.transform.smoothscale(black, (30, 30))
white = pygame.transform.smoothscale(white, (30, 30))

# 加载背景音乐
pygame.mixer.music.load('music/背景音乐.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1, 0)

# 加载音效
drop_sound = pygame.mixer.Sound('music/落子.WAV')
drop_sound.set_volume(0.3)
win = pygame.mixer.Sound('music/胜利.mp3')
win.set_volume(0.3)
lose = pygame.mixer.Sound('music/失败.mp3')
lose.set_volume(0.3)

# 设置矩形区域横坐标和纵坐标
button_rect = button.get_rect()
button_rect.x = 620
button_rect.y = 230


# 初始化变量
game = '游戏中'  # 游戏状态
status = 'black'  # 棋子颜色(1 代表黑棋，2 代表白棋)
result_status = 0

# 初始化列表
steps = []



gobang = []
# for 循环创建空二维列表
for i in range(WIDTH):
    row_list = []
    for j in range(HEIGHT):
        row_list.append(0)
    gobang.append(row_list)


# 主循环
while True:
    
    # 事件检测
    for event in pygame.event.get():
        # 退出游戏
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game != '游戏中':
                game = '游戏中'
                # 清空棋盘
                for i in range(WIDTH):
                    for j in range(HEIGHT):
                        gobang[i][j] = 0
                win.stop()
                lose.stop()
                pygame.mixer.music.play(-1, 0)
                result_status = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
             # 播放落子音效
            pos = pygame.mouse.get_pos()
            x = pos[0]
            y = pos[1]
            # 游戏中
            if game == '游戏中':
                if x <= 600:
                    row = y // 30
                    col = x // 30
                    if gobang[row][col] == 0:
                        gobang[row][col] = 1
                        # 入栈
                        steps.append([row, col])
                        drop_sound.play()

                        #电脑下棋
                        result = aiChess()
                        gobang[result[0]][result[1]] = 2
                        steps.append([result[0], result[1]])
                        # 播放落子音效
                        drop_sound.play()
            
            if button_rect.collidepoint(pos) and len(steps) != 0:
                if game != '游戏中':
                    pygame.mixer.music.play(-1, 0)
                    win.stop()
                    lose.stop()
                    result_status = 0
                # 同时退出一颗黑棋和一颗白棋
                # 出栈
                last = steps.pop()
                gobang[last[0]][last[1]] = 0
                # 出栈
                last = steps.pop()
                gobang[last[0]][last[1]] = 0
            

    # 绘制背景
    screen.blit(background,(0,0))

    # 绘制棋盘
    screen.blit(chessboard, (0, 0))

    # 绘制棋子
    for row in range(WIDTH):
        for col in range(HEIGHT):
            if gobang[row][col] == 1:
                screen.blit(black, (col * 30, row * 30))
            elif gobang[row][col] == 2:
                screen.blit(white, (col * 30, row * 30))

    # 画出按钮
    screen.blit(button, (button_rect.x, button_rect.y))  # 画出发型按钮
    
    # 检查游戏的状态
    game = check(gobang)

    # 游戏结束
    if game != '游戏中':
        if result_status == 0:
            pygame.mixer.music.stop()
            if game == '黑棋胜利':
                win.play()
            else:
                lose.play()
            result_status = 1
        # 显示游戏结果
        show_result(screen, game)
    
    

    # 更新屏幕
    pygame.display.update()
    
    
    

    

#student_code_ends