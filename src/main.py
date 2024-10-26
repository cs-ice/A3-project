import pygame
import sys
import image
import button
import poker
import inputbox
import os
import random

os.environ["SDL_IME_SHOW_UI"] = "1" # 显示输入候选框 0是False 1是True

'''==================================常量区================================================'''
SCREEN_HEIGHT = 800                     # 窗体大小
SCREEN_WIDTH = 1280

CARD_HEIGHT = 150                       # 卡牌的高度和宽度常量
CARD_WIDTH = 100

GAME_WAIT = 1                           # 游戏未开始 正在等待
GAME_READY = 0                          # 游戏准备状态
GAME_START = 0                          # 游戏开始执行


FPS = 60


BUTTON_SEND_X, BUTTON_SEND_Y = 550, 560
BUTTON_SEND_HEIGHT, BUTTON_SEND_WIDTH = 140, 60


'''=================================全局函数区=============================================='''


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


def update_handcard_draw(sprite_lst):              # 假设从x = 250开始绘制
    length_cards = len(sprite_lst)
    if CARD_WIDTH * length_cards > 750:                # 750是指牌组最多占据 750 x像素
        rect_width = 650 / length_cards                 # 最后一张牌占满100
        for i in sprite_lst:
            i.rect.x = 250 - rect_width
            i.rect.width = rect_width                   # 计算每张牌的矩形 宽度
        j = 1
        for i in sprite_lst:
            i.rect.x += rect_width * j                  # 移动每张矩形到达指定位置
            j +=1
        sprite_lst[length_cards - 1].rect.width = CARD_WIDTH
    else:                                               #以下是手牌较少的情况
        rect_width = CARD_WIDTH
        for i in sprite_lst:
            i.rect.x = 250 - rect_width
            i.rect.width = rect_width
        j = 1
        for i in sprite_lst:
            i.rect.x += rect_width * j
            j +=1


def update_rects(lst):
    pass

def update_deskcards_draw(card_lst, desk, order):             # 更新牌桌区      order 决定上下左右绘制   
    # 上470 170    下 470 400   左 200 330   右边 900 330   
    # 根据习惯 上下左右 1234

    if order == 1:
        x, y = (470, 170)
    elif order == 2:
        x, y = (470, 400)
    elif order == 3:
        x, y = (200, 330)
    elif order == 4:
        x, y = (900, 330)

    card_lst.sort()
    for id in card_lst:
        img = poker.Poker(f'pic\{get_suit(id)}\{get_name(id)}.png', (CARD_WIDTH / 1.5, CARD_HEIGHT / 1.5), (x, y), id)
        x += 60
        desk.add(img)

def mouse_select_cards(hand, event):                    # 参数1 手牌一个精灵组  参数二 事件对象 
    for i in hand:
        if i.rect.collidepoint(event.pos):
            i.move()
            print('ID:',i.get_ID())


'''=================================重要变量区================================='''
pygame.init()                               # 加载pygame
pygame.font.init()                          # 加载字体渲染
DS = pygame.display.set_mode(( SCREEN_WIDTH, SCREEN_HEIGHT))                    # 主屏
pygame.display.set_caption('A3')
GAME_bg = image.Image('pic\\gamebg.png', ( SCREEN_WIDTH, SCREEN_HEIGHT), (0,0))
WAIT_bg = image.Image('pic\\waitbg.jpg', ( SCREEN_WIDTH, SCREEN_HEIGHT), (0,0))
clock = pygame.time.Clock()                                                     # FPS时钟


buttonfont = pygame.font.SysFont('华文楷体', 50)
textfont = pygame.font.SysFont('华文楷体', 25)


SEND_CARD = buttonfont.render('出牌', True, (255, 255, 255))
SEND_START = buttonfont.render('快速开始', True, (255, 255, 255))
SEND_PASS = buttonfont.render('不出', True, (255, 255, 255))


button_start = button.Button( (520, 550), SEND_START, 1)
#ButtonStart1 = button.Button( (250, 100))
button_send = button.Button((BUTTON_SEND_X, BUTTON_SEND_Y), SEND_CARD, 1)
button_pass = button.Button((BUTTON_SEND_X+150, BUTTON_SEND_Y), SEND_PASS, 1)

inputbox_accout = inputbox.InputBox(DS, 470, 400, 300, 40, textfont)
inputbox_room = inputbox.InputBox(DS, 470, 450, 300, 40, textfont)



'''============================================================================='''
        
while GAME_WAIT:                                            # 等待界面

    for event in pygame.event.get():
        inputbox_accout.get_text(event)
        inputbox_room.get_text(event)
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass
 
    WAIT_bg.draw(DS)
    if button_start.draw(DS):
        print(inputbox_accout.return_text())
        GAME_WAIT = False

    inputbox_accout.draw()
    inputbox_room.draw()
    pygame.display.update()
    clock.tick(60)



lst = [random.randint(0,51) for _ in range(13)]
lst.sort()
hand = pygame.sprite.Group()
x = 250
for id in lst:
    ima = poker.Poker(f'pic\{get_suit(id)}\{get_name(id)}.png', (CARD_WIDTH, CARD_HEIGHT), (x, 800-150), id)
    x += 60
    hand.add(ima)



running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_select_cards(hand.sprites(), event)
            pass
    GAME_bg.draw(DS)
    if button_send.draw(DS):
        print('777')
    
 
    button_pass.draw(DS)
    update_handcard_draw(hand.sprites())
    
    hand.draw(DS)
    pygame.display.update()

    

