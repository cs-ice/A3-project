import pygame
import sys
import image
import button
import poker
import inputbox
import os
os.environ["SDL_IME_SHOW_UI"] = "1" # 显示输入候选框 0是False 1是True
'''==================================常量区================================================'''
SCREEN_HEIGHT = 720                    # 窗体大小
SCREEN_WIDTH = 1280
WIDTH_HEIGHT_RATIO = 16 / 9


CARD = pygame.image.load('pic\\3\\1.png')       # 加载一张原始卡牌
CARD_SELF_RATIO = CARD.get_width() / CARD.get_height()
CARD_SCREEN_RATIO = 150 / 800            # 计算卡牌比例 我希望卡牌高度占 150/800
CARD_HEIGHT = SCREEN_HEIGHT * CARD_SCREEN_RATIO    # 卡牌的高度和宽度常量
CARD_WIDTH = CARD_SELF_RATIO * CARD_HEIGHT




GAME_WAIT = 1                           # 游戏未开始 正在等待
GAME_READY = 0                          # 游戏准备状态
GAME_START = 0                          # 游戏开始执行


FPS = 60


BUTTON_SEND_X, BUTTON_SEND_Y = 550, 560
BUTTON_SEND_HEIGHT, BUTTON_SEND_WIDTH = 140, 60




'''=================================全局函数区=============================================='''
def get_relative_position(x, y, SCREEN_WIDTH ,SCREEN_HEIGHT, surface):                # x, y指的是占据到哪个位置
    return (x / SCREEN_WIDTH) * surface.get_width() , (y / SCREEN_HEIGHT) * surface.get_height()


def get_name(card_id):              # 根据ID获取文件名称
    a = card_id // 4 + 4
    if a == 14:
        a = 1
    elif a == 15:
        a = 2
    elif a == 16:
        a = 3
    return a

def get_point(card_id): 
    return card_id // 4            # 返回0是卡牌4， 返回12是卡牌3

def get_suit(card_id):
    return card_id %  4           # 3spade, 2heart, 1club, 0diamond


def update_handcard_draw(lst):              # 假设从x = 250开始绘制
    length_cards = len(lst)
    if CARD_WIDTH * length_cards > 750:                # 750是指牌组最多占据 750 x像素
        rect_width = 650 / length_cards                 # 最后一张牌占满100
        for i in lst:
            i.rect.x = 250 - rect_width
            i.rect.width = rect_width                   # 计算每张牌的矩形 宽度
        j = 1
        for i in lst:
            i.rect.x += rect_width * j                  # 移动每张矩形到达指定位置
            j +=1
        lst[length_cards - 1].rect.width = CARD_WIDTH
    else:                                               #以下是手牌较少的情况
        rect_width = CARD_WIDTH
        for i in lst:
            i.rect.x = 250 - rect_width
            i.rect.width = rect_width
        j = 1
        for i in lst:
            i.rect.x += rect_width * j
            j +=1


def update_rects(lst):
    pass

def update_deskcards_draw(card_lst, desk, order):             # 更新牌桌区      order 决定上下左右绘制   
    # 上470 170    下 470 400   左 200 280   右边 900 280   
    # 根据逆时针 下右上左  1234

    if order == 3:
        x, y = (470, 170)
    elif order == 1:
        x, y = (470, 400)
    elif order == 4:
        x, y = (200, 280)
    elif order == 2:
        x, y = (900, 280)

    card_lst.sort()
    for id in card_lst:
        img = poker.Poker(f'pic\{get_suit(id)}\{get_name(id)}.png', (150 / 800) / 1.5, (x, y), id)
        x += 60
        desk.add(img)



        


'''=================================重要变量区================================='''
pygame.init()                               # 加载pygame
pygame.font.init()                          # 加载字体渲染

DS = pygame.display.set_mode(( SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('A3')
GAME_bg = image.Image('pic\\gamebg.png', (SCREEN_WIDTH, SCREEN_HEIGHT), get_relative_position(0,0,SCREEN_WIDTH,SCREEN_HEIGHT,DS))
WAIT_bg = image.Image('pic\\waitbg.jpg', (SCREEN_WIDTH, SCREEN_HEIGHT), get_relative_position(0,0,SCREEN_WIDTH,SCREEN_HEIGHT,DS))
on_press_btn_1 = False
clock = pygame.time.Clock()


'''============================================================================='''


lst = [1,3,5,11,21,23,25,27,32,36,39,51, 0]

font = pygame.font.SysFont('华文楷体', 50)
font = pygame.font.SysFont('华文楷体', 20)
SEND_CARD = font.render('出牌', True, (255, 255, 255))
SEND_START = font.render('快速开始', True, (255, 255, 255))
ButtonStart = button.Button( (520, 400), SEND_START, 1)
#ButtonStart1 = button.Button( (250, 100))
ButtonSend = button.Button((BUTTON_SEND_X, BUTTON_SEND_Y), SEND_CARD, 1)
# 对于某些按钮需要缩放变换的 同时加载一张原图片和缩放后的图片 需要时切换即可

inp = inputbox.InputBox(DS, 200, 200, 300, 40, font)









x = 250

hand = pygame.sprite.Group()                    
desk = pygame.sprite.Group()
card_point = 2
for id in lst:
    ima = poker.Poker(f'pic\{get_suit(id)}\{get_name(id)}.png', (CARD_WIDTH, CARD_HEIGHT), (x, 800-150), id)
    x += 60
    card_point += 1
    hand.add(ima)
running = True

while GAME_WAIT:                                            # 等待界面

    
    for event in pygame.event.get():
        inp.get_text(event)
        if event.type == pygame.KEYDOWN:
            
            print(event.unicode)
        
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            new_width, new_height = event.w, event.h
            print(event.w, event.h)
            if new_width != SCREEN_WIDTH:
                new_height = new_width / WIDTH_HEIGHT_RATIO
                SCREEN_WIDTH = new_width
                print(999)
            else:
                new_width = new_height * WIDTH_HEIGHT_RATIO
                print(new_width/new_height)
            
            DS = pygame.display.set_mode((new_width,new_height), pygame.RESIZABLE)
            WAIT_bg = image.Image('pic\\waitbg.jpg', (new_width,new_height),  (0,0))
        elif event.type == pygame.MOUSEBUTTONDOWN:
            
            """ if event.button == 1:
                if ButtonStart.rect.collidepoint(event.pos):
                    GAME_WAIT = 0
        elif event.type == pygame.MOUSEMOTION:
            if ButtonStart.rect.collidepoint(event.pos):
                ButtonStart.is_selected = True
            else:
                ButtonStart.is_selected = False
            if ButtonStart.is_selected:
                ButtonStart.image = pygame.transform.scale(ButtonStart.image, (200, 100))
            else:
                ButtonStart.image = ButtonStart1.image """
 

    WAIT_bg.draw(DS)
    
    inp.draw()
    
    if ButtonStart.draw(DS):
        GAME_WAIT = False
    pygame.display.update()

    clock.tick(24)



desk_lst = []

iii = 1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            DS = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            GAME_bg = image.Image('pic\\gamebg.png', (event.w, event.h), get_relative_position(0,0,SCREEN_WIDTH,SCREEN_HEIGHT,DS))

        elif event.type == pygame.MOUSEBUTTONDOWN:
 
            if event.button == 1:
                for i in hand:
                    if i.rect.collidepoint(event.pos):
                        i.move()
                        print('ID:',i.get_ID())
            elif event.button == 3:
                pass
            update_handcard_draw(hand.sprites())
        elif event.type == pygame.MOUSEBUTTONUP:
            pass
        elif event.type == pygame.MOUSEMOTION:
            print(event.pos)
    
    if GAME_START:
        pass
    elif GAME_WAIT:
        pass
    elif GAME_READY:
        pass

    GAME_bg.draw(DS)
    if ButtonSend.draw(DS):
        print('777')
        for i in hand:
            
            if i.is_selected: 
                print(pygame.mouse.get_pos())                          # 选中的牌才能上Desk
                
                desk_lst.append(i.get_ID())
                hand.remove(i)
                update_deskcards_draw(desk_lst, desk, iii)
                iii += 1
                if iii == 5:
                    iii = 1
    if len(desk_lst) >=3:
        desk_lst = []
        desk.clear(DS, DS)
        print(888)
    hand.draw(DS)
    desk.draw(DS)
    desk.update()
    update_handcard_draw(hand.sprites())


    pygame.display.update()



