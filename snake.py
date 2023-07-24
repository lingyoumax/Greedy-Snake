import random
import pygame
import sys
from pygame.locals import *
from collections import deque


map_number = 2 # 网格倍数，map_number>=0.5
safe_distance = 7 # 初始蛇的安全距离
Block_left = 0.2 # 障碍左侧距屏幕左边的相对距离
Block_right = 0.3 # 障碍右侧距屏幕左边的相对距离
########

# 一块蛇身大小
Cell_Size = round(20/map_number)
# 屏幕大小
Window_Width = round(40 * map_number) * Cell_Size
Window_Height = round(25 * map_number) * Cell_Size


# # 屏幕大小
#Window_Width = 800
#Window_Height = 500
# 刷新频率
Display_Clock = 20  # 17
# # 一块蛇身大小
#Cell_Size = 50

assert Window_Width % Cell_Size == 0
assert Window_Height % Cell_Size == 0
Cell_W = int(Window_Width/Cell_Size)
Cell_H = int(Window_Height/Cell_Size)
# 背景颜色
Background_Color = (0, 0, 0)
# 蛇头索引
Head_index = 0

# 加方形障碍,用左右的相对位置来表征
# Block1=[{'x': round(Cell_W * 0.5), 'y': round(Cell_H * 0.5)}]
Block1 = []
Block_left_up_x1 = round(Cell_W * Block_left)
Block_left_up_y1 = round(Cell_H * Block_left)
Block_left_up_x2 = round(Cell_W * Block_right)
Block_left_up_y2 = round(Cell_H * Block_right)
for blocki in range(Block_left_up_x1, Block_left_up_x2, 1):
    for blockj in range(Block_left_up_y1, Block_left_up_y2, 1):
        newBlock =  {'x': blocki,
                            'y': blockj}
        Block1.insert(1, newBlock)
Block_right_up_x1 = round(Cell_W * (1 - Block_right))
Block_right_up_y1 = round(Cell_H * Block_left)
Block_right_up_x2 = round(Cell_W * (1 - Block_left))
Block_right_up_y2 = round(Cell_H * Block_right)
for blocki in range(Block_right_up_x1, Block_right_up_x2, 1):
    for blockj in range(Block_right_up_y1, Block_right_up_y2, 1):
        newBlock =  {'x': blocki,
                            'y': blockj}
        Block1.insert(1, newBlock)
Block_left_down_x1 = round(Cell_W * Block_left)
Block_left_down_y1 = round(Cell_H * (1 - Block_right))
Block_left_down_x2 = round(Cell_W * Block_right)
Block_left_down_y2 = round(Cell_H * (1 - Block_left))
for blocki in range(Block_left_down_x1, Block_left_down_x2, 1):
    for blockj in range(Block_left_down_y1, Block_left_down_y2, 1):
        newBlock =  {'x': blocki,
                            'y': blockj}
        Block1.insert(1, newBlock)
Block_right_down_x1 = round(Cell_W * (1 - Block_right))
Block_right_down_y1 = round(Cell_H * (1 - Block_right))
Block_right_down_x2 = round(Cell_W * (1 - Block_left))
Block_right_down_y2 = round(Cell_H * (1 - Block_left))
for blocki in range(Block_right_down_x1, Block_right_down_x2, 1):
    for blockj in range(Block_right_down_y1, Block_right_down_y2, 1):
        newBlock =  {'x': blocki,
                            'y': blockj}
        Block1.insert(1, newBlock)


# BLOCKx1 = 0
# BLOCKy1 = 5
# Block1 = [{'x': BLOCKx1, 'y': BLOCKy1},
#           {'x': BLOCKx1+1, 'y': BLOCKy1},
#           {'x': BLOCKx1+2, 'y': BLOCKy1},
#           {'x': BLOCKx1+3, 'y': BLOCKy1}]
# Block1.insert(0, newHead1)


# 关闭游戏界面
def close_game():
    pygame.quit()
    sys.exit()


# 检测玩家的按键
def Check_PressKey():
    if len(pygame.event.get(QUIT)) > 0:
        close_game()
    KeyUp_Events = pygame.event.get(KEYUP)
    if len(KeyUp_Events) == 0:
        return None
    elif KeyUp_Events[0].key == K_ESCAPE:
        close_game()
    return KeyUp_Events[0].key


# # 显示当前得分
# def Show_Score(score):
#     score_Content = Main_Font.render('得分：%s' % (score), True, (255, 255, 255))
#     score_Rect = score_Content.get_rect()
#     score_Rect.topleft = (Window_Width-120, 10)
#     Main_Display.blit(score_Content, score_Rect)
# 显示当前得分,位置再调
def Show_Score(score1, score2):
    score_Content = Main_Font.render(
        '得分1:%s 得分2:%s' % (score1, score2), True, (255, 255, 255))
    score_Rect = score_Content.get_rect()
    score_Rect.topleft = (Window_Width-220, 10)
    Main_Display.blit(score_Content, score_Rect)


# 获得果实位置
def Get_Apple_Location(snake_Coords):
    flag = True
    while flag:
        apple_location = {'x': random.randint(
            0, Cell_W-1), 'y': random.randint(0, Cell_H-1)}
        if (apple_location not in snake_Coords) and (apple_location not in Block1):
            flag = False
    return apple_location

# 显示果实
def Show_Apple(coord):
    x = coord['x'] * Cell_Size
    y = coord['y'] * Cell_Size
    apple_Rect = pygame.Rect(x, y, Cell_Size, Cell_Size)
    pygame.draw.rect(Main_Display, (255, 0, 0), apple_Rect)

# 显示蛇
def Show_Snake_single(coords1):
    x1 = coords1[0]['x'] * Cell_Size
    y1 = coords1[0]['y'] * Cell_Size
    # 头是实心蓝色
    Snake_head_Rect1 = pygame.Rect(x1, y1, Cell_Size, Cell_Size)
    pygame.draw.rect(Main_Display, (0, 80, 255), Snake_head_Rect1)
    Snake_head_Inner_Rect1 = pygame.Rect(x1+4, y1+4, Cell_Size-8, Cell_Size-8)
    pygame.draw.rect(Main_Display, (0, 80, 255), Snake_head_Inner_Rect1)
    for coord in coords1[1:]:
        x = coord['x'] * Cell_Size
        y = coord['y'] * Cell_Size
        Snake_part_Rect = pygame.Rect(x, y, Cell_Size, Cell_Size)
        pygame.draw.rect(Main_Display, (0, 155, 0), Snake_part_Rect)
        Snake_part_Inner_Rect = pygame.Rect(x+4, y+4, Cell_Size-8, Cell_Size-8)
        pygame.draw.rect(Main_Display, (0, 255, 0), Snake_part_Inner_Rect)

def Show_Snake(coords1, coords2):
    x1 = coords1[0]['x'] * Cell_Size
    y1 = coords1[0]['y'] * Cell_Size
    # 头是实心蓝色
    Snake_head_Rect1 = pygame.Rect(x1, y1, Cell_Size, Cell_Size)
    pygame.draw.rect(Main_Display, (0, 80, 255), Snake_head_Rect1)
    Snake_head_Inner_Rect1 = pygame.Rect(x1+4, y1+4, Cell_Size-8, Cell_Size-8)
    pygame.draw.rect(Main_Display, (0, 80, 255), Snake_head_Inner_Rect1)
    for coord in coords1[1:]:
        x = coord['x'] * Cell_Size
        y = coord['y'] * Cell_Size
        Snake_part_Rect = pygame.Rect(x, y, Cell_Size, Cell_Size)
        pygame.draw.rect(Main_Display, (0, 155, 0), Snake_part_Rect)
        Snake_part_Inner_Rect = pygame.Rect(x+4, y+4, Cell_Size-8, Cell_Size-8)
        pygame.draw.rect(Main_Display, (0, 255, 0), Snake_part_Inner_Rect)
    # 2还没改颜色，黄色(255, 255, 0)紫色(255, 0,255),橘色框黄色芯
    x2 = coords2[0]['x'] * Cell_Size
    y2 = coords2[0]['y'] * Cell_Size
    Snake_head_Rect2 = pygame.Rect(x2, y2, Cell_Size, Cell_Size)
    pygame.draw.rect(Main_Display, (255, 0, 255), Snake_head_Rect2)
    Snake_head_Inner_Rect2 = pygame.Rect(
        x2+4, y2+4, Cell_Size-8, Cell_Size-8)  # 这个才是里面的？
    pygame.draw.rect(Main_Display, (255, 0, 255), Snake_head_Inner_Rect2)
    for coord in coords2[1:]:
        x = coord['x'] * Cell_Size
        y = coord['y'] * Cell_Size
        Snake_part_Rect = pygame.Rect(x, y, Cell_Size, Cell_Size)
        pygame.draw.rect(Main_Display, (255, 155, 0), Snake_part_Rect)
        Snake_part_Inner_Rect = pygame.Rect(x+4, y+4, Cell_Size-8, Cell_Size-8)
        pygame.draw.rect(Main_Display, (255, 255, 0), Snake_part_Inner_Rect)

def Show_Block(Block):
    for block in Block[0:]:
        x = block['x'] * Cell_Size
        y = block['y'] * Cell_Size
        Block_part = pygame.Rect(x, y, Cell_Size, Cell_Size)
        pygame.draw.rect(Main_Display, (255, 255, 255), Block_part)
        Block_part_Inner = pygame.Rect(x+4, y+4, Cell_Size-8, Cell_Size-8)
        pygame.draw.rect(Main_Display, (190, 190, 190), Block_part_Inner)

# 画网格
def draw_Grid():
    # 垂直方向
    for x in range(0, Window_Width, Cell_Size):
        pygame.draw.line(Main_Display, (40, 40, 40),
                         (x, 0), (x, Window_Height))
    # 水平方向
    for y in range(0, Window_Height, Cell_Size):
        pygame.draw.line(Main_Display, (40, 40, 40), (0, y), (Window_Width, y))

    # 障碍灰色（190,190,190）白色(255, 255, 255)

    # for i in range(Cell_Size*0, Cell_Size*3):
    #     Block_part = pygame.Rect(i, Cell_Size*5, Cell_Size, Cell_Size)
    #     pygame.draw.rect(Main_Display, (190, 190, 190), Block_part)
    # Block1 = [{'x': BLOCKx1, 'y': BLOCKy1},
    #           {'x': BLOCKx1+1, 'y': BLOCKy1},
    #           {'x': BLOCKx1-1, 'y': BLOCKy1}]
    # for block in Block1[0:]:
    #     x = block['x'] * Cell_Size
    #     y = block['y'] * Cell_Size
    #     Block_part = pygame.Rect(x, y, Cell_Size, Cell_Size)
    #     pygame.draw.rect(Main_Display, (255, 155, 0), Block_part)
    #     Block_part_Inner = pygame.Rect(x+4, y+4, Cell_Size-8, Cell_Size-8)
    #     pygame.draw.rect(Main_Display, (255, 255, 0), Block_part_Inner)



# 显示开始界面
display_width = 1200
display_height = 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
pygame.init()
Button_Font = pygame.font.Font('simHei.ttf', 60)


class Button(object):
	def __init__(self, text, color, x=None, y=None, **kwargs):
		self.surface = Button_Font.render(text, True, color)

		self.WIDTH = self.surface.get_width()
		self.HEIGHT = self.surface.get_height()

		if 'centered_x' in kwargs and kwargs['centered_x']:
			self.x = display_width // 2 - self.WIDTH // 2
		else:
			self.x = x
		if 'centered_y' in kwargs and kwargs['cenntered_y']:
			self.y = display_height // 2 - self.HEIGHT // 2
		else:
			self.y = y

	def display(self):
		Main_Display.blit(self.surface, (self.x, self.y))
	def check_click(self, position):
		x_match = position[0] > self.x and position[0] < self.x + self.WIDTH
		y_match = position[1] > self.y and position[1] < self.y + self.HEIGHT
		if x_match and y_match:
			return True
		else:
			return False

def Show_Start_Interface():
    title_Font = pygame.font.Font('simHei.ttf', 100)
    title_content = title_Font.render('贪吃蛇', True, (255, 255, 255), (0, 0, 160))
    Main_Display.blit(title_content, (display_width//2 - title_content.get_width()//2, 150))

    mode1_button = Button('single_snake', RED, None, 350, centered_x=True)
    mode2_button = Button('pvp_game', WHITE, None, 400, centered_x=True)

    mode1_button.display()
    mode2_button.display()
    pygame.display.update()

    while True:
        if mode1_button.check_click(pygame.mouse.get_pos()):
            mode1_button = Button('single_snake', RED, None, 350, centered_x=True)
        else:
            mode1_button = Button('single_snake', WHITE, None, 350, centered_x=True)
        if mode2_button.check_click(pygame.mouse.get_pos()):
            mode2_button = Button('pvp_game', RED, None, 400, centered_x=True)
        else:
            mode2_button = Button('pvp_game', WHITE, None, 400, centered_x=True)

        mode1_button.display()
        mode2_button.display()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
        if pygame.mouse.get_pressed()[0]:
            if mode1_button.check_click(pygame.mouse.get_pos()):
                global AI_mode
                AI_mode= True
                return
            if mode2_button.check_click(pygame.mouse.get_pos()):
                AI_mode= False
                return




# 显示结束界面
def Show_End_Interface():
    if AI_mode==True:
        title_Font = pygame.font.Font('simHei.ttf', 100)
        title_game = title_Font.render('AI_snake DEAD', True, (233, 150, 122))
        game_Rect = title_game.get_rect()
        game_Rect.midtop = (Window_Width/2, 70)
        Main_Display.blit(title_game, game_Rect)
        pressKey_content = Main_Font.render('按任意键开始游戏！', True, (255, 255, 255))
        pressKey_Rect = pressKey_content.get_rect()
        pressKey_Rect.topleft = (Window_Width-200, Window_Height-30)
        Main_Display.blit(pressKey_content, pressKey_Rect)
        pygame.display.update()
        pygame.time.wait(500)
        # 清除事件队列
        Check_PressKey()
        while True:
            if Check_PressKey():
                pygame.event.get()
                return
    else:
        title_Font = pygame.font.Font('simHei.ttf', 100)
        title_game = title_Font.render('Game', True, (233, 150, 122))
        title_over = title_Font.render('Over', True, (233, 150, 122))
        game_Rect = title_game.get_rect()
        over_Rect = title_over.get_rect()
        game_Rect.midtop = (Window_Width/2, 70)
        over_Rect.midtop = (Window_Width/2, game_Rect.height+70+25)
        Main_Display.blit(title_game, game_Rect)
        Main_Display.blit(title_over, over_Rect)
        pressKey_content = Main_Font.render('按任意键开始游戏！', True, (255, 255, 255))
        pressKey_Rect = pressKey_content.get_rect()
        pressKey_Rect.topleft = (Window_Width-200, Window_Height-30)
        Main_Display.blit(pressKey_content, pressKey_Rect)
        pygame.display.update()
        pygame.time.wait(500)
        # 清除事件队列
        Check_PressKey()
        while True:
            if Check_PressKey():
                pygame.event.get()
                return

def choose_direction(snake_Coords1, apple_location1,direction1):
    x_h=snake_Coords1[Head_index]['x']
    y_h=snake_Coords1[Head_index]['y']
    x_d=0#按照当前运动方向预测下一步坐标，保持一定的“惯性”
    y_d=0
    if direction1=='left':
        x_d=-1
    elif direction1=='right':
        x_d=1
    elif direction1=='up':
        y_d=-1
    elif direction1=='down':
        y_d=1
    nodelist=[{'x':x_h-1,'y':y_h},{'x':x_h+1,'y':y_h},{'x':x_h,'y':y_h-1},{'x':x_h,'y':y_h+1}]
    n=[]
    for i in nodelist:
        def is_deadend(i):#单步a*判断死路
            NodeSet=[i]
            PreSet=[]
            TempList=[{'x':i['x']-1,'y':i['y']},
                    {'x':i['x']+1,'y':i['y']},
                    {'x':i['x'],'y':i['y']-1},
                    {'x':i['x'],'y':i['y']+1}]
            for t in TempList:
                if t==snake_Coords1[-1]:
                    return False
                elif (t['x'] == -1) or (t['x'] == Cell_W) or (t['y'] == -1) or (t['y'] == Cell_H):
                    continue  # 1碰壁
                elif t in snake_Coords1[0:len(snake_Coords1)-1]:
                    continue  # 1碰自己
                elif t in Block1[0:]:
                    continue
                else:
                    PreSet.append({'x':t['x'],'y':t['y'],'f':abs(t['x']-snake_Coords1[-1]['x'])+abs(t['y']-snake_Coords1[-1]['y'])}) 
            PreSet.sort(key=lambda x: x['f'])
            while len(PreSet)>0:
                temp=PreSet[0]
                del PreSet[0]
                NodeSet.append({'x':temp['x'],'y':temp['y']})
                TempList=[{'x':temp['x']-1,'y':temp['y']},
                        {'x':temp['x']+1,'y':temp['y']},
                        {'x':temp['x'],'y':temp['y']-1},
                        {'x':temp['x'],'y':temp['y']+1}]
                for t in TempList:
                    if t==snake_Coords1[-1]:
                        return False
                    elif (t['x'] == -1) or (t['x'] == Cell_W) or (t['y'] == -1) or (t['y'] == Cell_H):
                        continue  # 1碰壁
                    elif t in snake_Coords1[0:len(snake_Coords1)-1]:
                        continue  # 1碰自己
                    elif t in Block1[0:]:
                        continue
                    elif t in NodeSet or {'x':t['x'],'y':t['y'],'f':abs(t['x']-snake_Coords1[-1]['x'])+abs(t['x']-snake_Coords1[-1]['x'])} in PreSet:
                        continue
                    else:
                        for index in range(len(PreSet)):#插入算法，不使用排序，将时间复杂度由O(nlogn)降为O(n)
                            if PreSet[index]['f']>abs(t['x']-snake_Coords1[-1]['x'])+abs(t['x']-snake_Coords1[-1]['x']):
                                PreSet.insert(index,{'x':t['x'],'y':t['y'],'f':abs(t['x']-snake_Coords1[-1]['x'])+abs(t['x']-snake_Coords1[-1]['x'])})
                                break
                        else:
                            PreSet.insert(len(PreSet),{'x':t['x'],'y':t['y'],'f':abs(t['x']-snake_Coords1[-1]['x'])+abs(t['x']-snake_Coords1[-1]['x'])})
            return True
        if (i['x'] == -1) or (i['x'] == Cell_W) or (i['y'] == -1) or (i['y'] == Cell_H):
            continue  # 1碰壁
        elif {'x':i['x'],'y':i['y']} in snake_Coords1[1:]:
            continue  # 1碰自己
        elif {'x':i['x'],'y':i['y']} in Block1[0:]:
            continue
        elif is_deadend(i):
            continue
        else:
            n.append({'x':i['x']-x_h,'y':i['y']-y_h,'f':abs(i['x']-apple_location1['x'])+abs(i['y']-apple_location1['y'])})#单步A*算法的G值恒为0，F值即为H值
    if len(n)>0:
        n.sort(key=lambda x:x['f'])
        for i in range(len(n)-1,0,-1):
            if n[i]['f']>n[0]['f']:
                del n[i]
            else:
                break
        for i in n:
            if x_d==i['x'] and y_d==i['y']:
                return 'K_'+direction1.upper()#防止贪吃蛇“抽风”式前进，不美观，保持原有方向使得其直线运动
        else:
            node=random.choice(n)#因为单步的A-star算法有可能陷入局部最优，通过随机函数使得它有机会跳出局部最优，参考模拟退火算法
        if node['x']==1:
            return K_RIGHT
        elif node['x']==-1:
            return K_LEFT
        elif node['y']==1:
            return K_DOWN
        else:
            return K_UP
    else:
        return random.choice([K_UP,K_DOWN,K_RIGHT,K_LEFT]) 

# 运行游戏
def Run_Game():
    if AI_mode==True:
        # 蛇出生地，设置不能离墙或者block太近
        # start_x1 = random.randint(5, Cell_W-6)
        # start_y1 = random.randint(5, Cell_H-6)
        start_x1 = random.randint(safe_distance, Cell_W - safe_distance - 1)
        start_y1 = random.randint(safe_distance, Cell_H - safe_distance - 1)
        block_start1 = False
        for block in Block1[0:]:
            if (block['x'] - safe_distance < start_x1 < block['x'] + safe_distance) and (
                    block['y'] - safe_distance < start_y1 < block['y'] + safe_distance):
                block_start1 = True
        if block_start1:
            flag1 = True
        else:
            flag1 = False

        snake_Coords1 = [{'x': start_x1, 'y': start_y1},
                        {'x': start_x1-1, 'y': start_y1},
                        {'x': start_x1-2, 'y': start_y1}]
        direction1 = 'right'

        apple_location1 = Get_Apple_Location(snake_Coords1)  # 根据1号蛇产生的水果，不产生在头上

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    close_game()
                    ##!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            AI_dir = choose_direction(snake_Coords1, apple_location1,direction1)

            if (AI_dir == K_LEFT) and (direction1 != 'right'):
                direction1 = 'left'
            elif (AI_dir == K_RIGHT) and (direction1 != 'left'):
                direction1 = 'right'
            elif (AI_dir == K_UP) and (direction1 != 'down'):
                direction1 = 'up'
            elif (AI_dir == K_DOWN) and (direction1 != 'up'):
                direction1 = 'down'

            # 碰到墙壁、自己或障碍则游戏结束
            if (snake_Coords1[Head_index]['x'] == -1) or (snake_Coords1[Head_index]['x'] == Cell_W) or \
            (snake_Coords1[Head_index]['y'] == -1) or (snake_Coords1[Head_index]['y'] == Cell_H):
                return  # 1碰壁
            if snake_Coords1[Head_index] in snake_Coords1[1:]:
                return  # 1碰自己
            if snake_Coords1[Head_index] in Block1[0:]:
                return  # 1碰障碍
            if ((snake_Coords1[Head_index]['x'] == apple_location1['x']) and (snake_Coords1[Head_index]['y'] == apple_location1['y'])):
                apple_location1 = Get_Apple_Location(
                    snake_Coords1)  # 1头吃到水果1，新生成一个
            else:
                del snake_Coords1[-1]  # 删除变量、列表、字典等Python对象,应该直接game over
            if direction1 == 'up':
                newHead1 = {'x': snake_Coords1[Head_index]['x'],
                            'y': snake_Coords1[Head_index]['y']-1}
            elif direction1 == 'down':
                newHead1 = {'x': snake_Coords1[Head_index]['x'],
                            'y': snake_Coords1[Head_index]['y']+1}
            elif direction1 == 'left':
                newHead1 = {'x': snake_Coords1[Head_index]['x']-1,
                            'y': snake_Coords1[Head_index]['y']}
            elif direction1 == 'right':
                newHead1 = {'x': snake_Coords1[Head_index]['x']+1,
                            'y': snake_Coords1[Head_index]['y']}

            snake_Coords1.insert(0, newHead1)
            Main_Display.fill(Background_Color)
            draw_Grid()
            Show_Block(Block1)
            Show_Snake_single(snake_Coords1)  # 一次显示
            Show_Apple(apple_location1)

            pygame.display.update()
            Snake_Clock.tick(Display_Clock)
    else:
        # 蛇出生地，第一条蛇不能离墙或障碍太近，第二条蛇不能离墙、障碍或第一条蛇太近
        flag1 = True
        while flag1:
            start_x1 = random.randint(safe_distance, Cell_W - safe_distance - 1)
            start_y1 = random.randint(safe_distance, Cell_H - safe_distance - 1)
            block_start1 = False
            for block in Block1[0:]:
                if (block['x'] - safe_distance < start_x1 < block['x'] + safe_distance) and (
                        block['y'] - safe_distance < start_y1 < block['y'] + safe_distance):
                    block_start1 = True
            if block_start1:
                flag1 = True
            else:
                flag1 = False
        snake_Coords1 = [{'x': start_x1, 'y': start_y1},
                         {'x': start_x1 - 1, 'y': start_y1},
                         {'x': start_x1 - 2, 'y': start_y1}]
        direction1 = 'right'
        flag2 = True
        while flag2:
            start_x2 = random.randint(safe_distance, Cell_W - safe_distance - 1)
            start_y2 = random.randint(safe_distance, Cell_H - safe_distance - 1)
            block_start2 = False
            for block in Block1[0:]:
                if (block['x'] - safe_distance < start_x2 < block['x'] + safe_distance) and (
                        block['y'] - safe_distance < start_y2 < block['y'] + safe_distance):
                    block_start2 = True
            if (start_x1 - safe_distance < start_x2 < start_x1 + safe_distance) and (
                    start_y1 - safe_distance < start_y2 < start_y1 + safe_distance):
                flag2 = True
            elif block_start2:
                flag2 = True
            else:
                flag2 = False
        snake_Coords2 = [{'x': start_x2, 'y': start_y2},
                        {'x': start_x2, 'y': start_y2-1},
                        {'x': start_x2, 'y': start_y2-2}]
        direction2 = 'down'
        apple_location1 = Get_Apple_Location(snake_Coords1)  # 根据1号蛇产生的水果，不产生在头上
        apple_location2 = Get_Apple_Location(snake_Coords2)  # 根据2号蛇产生的水果


        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    close_game()
                elif event.type == KEYDOWN:
                    if (event.key == K_LEFT) and (direction1 != 'right'):
                        direction1 = 'left'
                    elif (event.key == K_RIGHT) and (direction1 != 'left'):
                        direction1 = 'right'
                    elif (event.key == K_UP) and (direction1 != 'down'):
                        direction1 = 'up'
                    elif (event.key == K_DOWN) and (direction1 != 'up'):
                        direction1 = 'down'
                    elif (event.key == ord('a')) and (direction2 != 'right'):
                        direction2 = 'left'
                    elif (event.key == ord('d')) and (direction2 != 'left'):
                        direction2 = 'right'
                    elif (event.key == ord('w')) and (direction2 != 'down'):
                        direction2 = 'up'
                    elif (event.key == ord('s')) and (direction2 != 'up'):
                        direction2 = 'down'
                    elif event.key == K_ESCAPE:
                        close_game()
            # 碰到墙壁、自己或障碍则游戏结束
            if (snake_Coords1[Head_index]['x'] == -1) or (snake_Coords1[Head_index]['x'] == Cell_W) or \
            (snake_Coords1[Head_index]['y'] == -1) or (snake_Coords1[Head_index]['y'] == Cell_H):
                return  # 1碰壁
            if (snake_Coords2[Head_index]['x'] == -1) or (snake_Coords2[Head_index]['x'] == Cell_W) or \
            (snake_Coords2[Head_index]['y'] == -1) or (snake_Coords2[Head_index]['y'] == Cell_H):
                return  # 2碰壁
            if snake_Coords1[Head_index] in snake_Coords1[1:]:
                return  # 1碰自己
            if snake_Coords2[Head_index] in snake_Coords2[1:]:
                return  # 2碰自己
            if snake_Coords1[Head_index] in snake_Coords2[1:]:
                return  # 1碰对方
            if snake_Coords2[Head_index] in snake_Coords1[1:]:
                return  # 2碰对方
            if snake_Coords1[Head_index] in Block1[0:]:
                return  # 1碰障碍
            if snake_Coords2[Head_index] in Block1[0:]:
                return  # 2碰障碍
            #吃水果长身体
            if ((snake_Coords1[Head_index]['x'] == apple_location1['x']) and (
                    snake_Coords1[Head_index]['y'] == apple_location1['y'])):
                apple_location1 = Get_Apple_Location(
                    snake_Coords1)  # 1头吃到水果1，新生成一个
            elif (snake_Coords1[Head_index]['x'] == apple_location2['x']) and (
                    snake_Coords1[Head_index]['y'] == apple_location2['y']):
                apple_location2 = Get_Apple_Location(
                    snake_Coords1)  # 1头吃到水果2，新生成一个
            else:
                del snake_Coords1[-1]
            if (snake_Coords2[Head_index]['x'] == apple_location1['x']) and (
                    snake_Coords2[Head_index]['y'] == apple_location1['y']):
                apple_location1 = Get_Apple_Location(
                    snake_Coords2)  # 2头吃到水果1，新生成一个
            elif ((snake_Coords2[Head_index]['x'] == apple_location2['x']) and (
                    snake_Coords2[Head_index]['y'] == apple_location2['y'])):
                apple_location2 = Get_Apple_Location(
                    snake_Coords2)  # 2头吃到水果2，新生成一个
            else:
                del snake_Coords2[-1]  # 删除变量、列表、字典等Python对象,应该直接game over

            if direction1 == 'up':
                newHead1 = {'x': snake_Coords1[Head_index]['x'],
                            'y': snake_Coords1[Head_index]['y']-1}
            elif direction1 == 'down':
                newHead1 = {'x': snake_Coords1[Head_index]['x'],
                            'y': snake_Coords1[Head_index]['y']+1}
            elif direction1 == 'left':
                newHead1 = {'x': snake_Coords1[Head_index]['x']-1,
                            'y': snake_Coords1[Head_index]['y']}
            elif direction1 == 'right':
                newHead1 = {'x': snake_Coords1[Head_index]['x']+1,
                            'y': snake_Coords1[Head_index]['y']}
            if direction2 == 'up':
                newHead2 = {'x': snake_Coords2[Head_index]['x'],
                            'y': snake_Coords2[Head_index]['y']-1}
            elif direction2 == 'down':
                newHead2 = {'x': snake_Coords2[Head_index]['x'],
                            'y': snake_Coords2[Head_index]['y']+1}
            elif direction2 == 'left':
                newHead2 = {'x': snake_Coords2[Head_index]['x']-1,
                            'y': snake_Coords2[Head_index]['y']}
            elif direction2 == 'right':
                newHead2 = {'x': snake_Coords2[Head_index]['x']+1,
                            'y': snake_Coords2[Head_index]['y']}

            snake_Coords1.insert(0, newHead1)
            snake_Coords2.insert(0, newHead2)
            Main_Display.fill(Background_Color)
            draw_Grid()
            Show_Block(Block1)
            Show_Snake(snake_Coords1, snake_Coords2)  # 一次显示
            Show_Apple(apple_location1)
            # Show_Score(len(snake_Coords1)-3)
            # Show_Snake(snake_Coords2)
            Show_Apple(apple_location2)
            # show_score改为两个一行展示
            Show_Score(len(snake_Coords1)-3, len(snake_Coords2)-3)
            pygame.display.update()
            Snake_Clock.tick(Display_Clock)



# 主函数
def main():
    global Main_Display, Main_Font, Snake_Clock
    pygame.init()
    Snake_Clock = pygame.time.Clock()
    Main_Display = pygame.display.set_mode((Window_Width, Window_Height))
    Main_Font = pygame.font.Font('simHei.ttf', 18)
    pygame.display.set_caption('Normal_snake')
    Show_Start_Interface()
    while True:
        Run_Game()
        Show_End_Interface()


if __name__ == '__main__':
    main()