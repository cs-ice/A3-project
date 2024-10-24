import pygame
import sys
import image
import Button
import poker
'''==================================常量区================================================'''
SCREEN_HEIGHT = 800                     # 窗体大小
SCREEN_WIDTH = 1280

CARD_HEIGHT = 150                       # 卡牌的高度和宽度常量
CARD_WIDTH = 100

GAME_WAIT = 1                           # 游戏未开始 正在等待
GAME_READY = 0                          # 游戏准备状态
GAME_START = 0                          # 游戏开始执行


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


def update_handcard_draw(lst):              # 假设从x = 250开始绘制
    length_cards = len(lst)
    if CARD_WIDTH * length_cards > 750:
        rect_width = 650 / length_cards
        for i in lst:
            i.rect.x = 250 - rect_width
            i.rect.width = rect_width
        j = 1
        for i in lst:
            i.rect.x += rect_width * j
            j +=1
        lst[length_cards - 1].rect.width = CARD_WIDTH
    else:
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

def update_deskcards_draw(card_lst, desk):             # 更新牌桌区
    x = 250
    card_lst.sort()
    for id in card_lst:
        img = poker.Poker(f'pic\{get_suit(id)}\{get_name(id)}.png', (CARD_WIDTH / 1.5, CARD_HEIGHT / 1.5), (x, 400), id)
        x += 60
        desk.add(img)



        


'''=================================重要变量区================================='''
pygame.init()                               # 加载pygame
pygame.font.init()                          # 加载字体渲染
print(pygame.font.get_fonts())
DS = pygame.display.set_mode(( SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('A3')
GAME_bg = image.Image('pic\\gamebg.png', ( SCREEN_WIDTH, SCREEN_HEIGHT), (0,0))
WAIT_bg = image.Image('pic\\waitbg.jpg', ( SCREEN_WIDTH, SCREEN_HEIGHT), (0,0))
on_press_btn_1 = False


'''============================================================================='''



ButtonStart = Button.Button('pic\kuaisu_choose.png', (250, 100), (500,400))
ButtonStart1 = Button.Button('pic\kuaisu_choose.png', (250, 100), (500,400))
ButtonSend = Button.Button('pic\\btn1.png', (BUTTON_SEND_HEIGHT, BUTTON_SEND_WIDTH), (BUTTON_SEND_X, BUTTON_SEND_Y))
# 对于某些按钮需要缩放变换的 同时加载一张原图片和缩放后的图片 需要时切换即可





text = ' 出牌'

lst = [1,3,5,11,21,23,25,27,32,36,39,51, 0]

font = pygame.font.SysFont('华文行楷', 50)

a = font.render(text, True, (255, 255, 255))
ButtonSend.image.blit(a, ButtonSend.rect)

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
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
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
                ButtonStart.image = ButtonStart1.image
 

    WAIT_bg.draw(DS)
    ButtonStart.draw(DS)
    pygame.display.update()



desk_lst = []



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass


            if event.button == 1:
                for i in hand:
                    if i.rect.collidepoint(event.pos):
                        i.move()
                        print('ID:',i.get_ID())
            elif event.button == 3:
                for i in hand:
                    if i.is_selected:                           # 选中的牌才能上Desk
                        if i.rect.collidepoint(event.pos):
                            if len(desk_lst) >=3:
                                desk_lst = []
                                desk.clear(DS, DS)
                                print(888)
                            desk_lst.append(i.get_ID())
                            hand.remove(i)
                            update_deskcards_draw(desk_lst, desk)
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
    ButtonSend.font_draw()
    ButtonSend.draw(DS)
    
    hand.draw(DS)
    desk.draw(DS)
    update_handcard_draw(hand.sprites())
    ButtonSend.image.blit(a, ButtonSend.rect)
    pygame.display.update()



