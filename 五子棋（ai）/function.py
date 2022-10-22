import pygame


# 绘制游戏结果
def show_result(screen, result):
    ft_font1 = pygame.font.Font('font/方正.TTF', 40)
    ft_surf1 = ft_font1.render(result, 1, (128,0,0))
    screen.blit(ft_surf1, (625, 180))
    ft_surf2 = ft_font1.render('按R重玩', 1, (128,0,0))
    screen.blit(ft_surf2, (625, 320))

# 判断是否五个棋子连续
def is_win(gobang, number):
    size = 20
    for n in range(size):
        # 判断垂直方向
        flag = 0
        for b in gobang:
            if b[n] == number:
                flag += 1
                if flag == 5:
                    return True
            else:
                flag = 0

        # 判断水平方向
        flag = 0
        for b in gobang[n]:
            if b == number:
                flag += 1
                if flag == 5:
                    return True
            else:
                flag = 0

        # 判断正斜方向
        for x in range(5 - 1, 2 * size - 5):
            flag = 0
            for i,b in enumerate(gobang):
                if size - 1 >= x - i >= 0 and b[x - i] == number:
                    flag += 1
                    if flag == 5:
                        return True
                else:
                    flag = 0

        #判断反斜方向
        for x in range(size - 5 + 1, 5 - size - 1, -1):
            flag = 0
            for i,b in enumerate(gobang):
                if 0 <= x + i <= size - 1 and b[x + i] == number:
                    flag += 1
                    if flag == 5:
                        return True
                else:
                    flag = 0
    return False

# 判断游戏胜利
def check(gobang):
    result = '游戏中'
    if gobang != []:
        # 判断玩家 1 是否胜利
        if is_win(gobang, 1):
            result = '黑棋胜利'
        # 判断玩家 2 是否胜利
        elif is_win(gobang, 2):
            result = '白棋胜利'
        # 判断是否平局
        else:
            count = 0
            for i in range(10):
                for j in range(10):
                    if gobang[i][j] != 0:
                        count += 1
            if count == 100:
                result = '平局'

    return result

#显示列表数字
def show_list(screen,gobang:list):
    ft_font1 = pygame.font.Font('font/方正.TTF', 40)
    for row in range(10):
        for col in range(10):
            ft_surf1 = ft_font1.render(str(gobang[col][row]), 1, (242, 235, 212))
            screen.blit(ft_surf1, (row * 60 + 15, col * 60 + 10))

def mouse_chess( position, screen, img):
    pygame.mouse.set_visible(False)
    screen.blit(img, (position[0] - 30, position[1] - 30))