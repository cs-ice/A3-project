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


'''==================================常量区================================================'''
SCREEN_HEIGHT = 720                    # 窗体大小
SCREEN_WIDTH = 1280
WIDTH_HEIGHT_RATIO = 16 / 9


CARD_HEIGHT = 150    # 卡牌的高度和宽度常量
CARD_WIDTH = 100




GAME_WAIT = 1                           # 游戏未开始 正在等待
GAME_READY = 0                          # 游戏准备状态
GAME_START = 0                          # 游戏开始执行


FPS = 60


BUTTON_SEND_X, BUTTON_SEND_Y = 550, 560
BUTTON_SEND_HEIGHT, BUTTON_SEND_WIDTH = 140, 60


'''================================================================================'''



import pygame
from image import *
import sys


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.Clock = pygame.time.Clock()

        self.handcards = [x+9 for x in range(13)]                                     # 手牌的ID列表
        self.handcards_images = {}                              # 手牌的图像字典   格式{ID： Image}
        self.handcards_length = 0                  # 手牌长度 用于检测手牌长度变化 若变化就更新手牌绘制

    '''
    若手牌数量发生变化  更新手牌的位置
    '''
    def update_handcard_rect(self):
        curr_handcards_len = len(self.handcards)
        print(self.handcards_length)
        if curr_handcards_len == self.handcards_length:        # 若当前手牌数 等于上一次的手牌长度 return退出
            return
        
        # 这意味着 self.handcards_length 只能在本方法更新
        self.handcards_length = curr_handcards_len             # 先更新 length

        # 1. 先算矩形宽度 高度不用管
        if CARD_WIDTH * curr_handcards_len >= 750:             # 人为规定为 手牌总长度最大750
            card_rect_width = 650 / curr_handcards_len         # 最后一张占满100 所以只剩650
        else:
            card_rect_width = 100                              # 否则直接铺满100

        # 2. 再算x坐标 y不用管                         
        xpos_lst = [250 + card_rect_width * i for i in range(curr_handcards_len)]# x从250开始绘制
        print(xpos_lst)
        i = 0
        for id in self.handcards:
            self.handcards_images[id].set_rect(xpos_lst[i], 720-150, card_rect_width, 150)
            i += 1

        self.handcards_images[self.handcards[i-1]].set_rect(xpos_lst[i-1], 720-150, 100, 150)      # 最后一张永远是100


    '''
    通过一组卡牌的ID  更新一个{ID: Image} 字典
    
    这用于发牌的时候初始化手牌
    '''
    def handcards_to_images(self):
        for id in self.handcards:
            img = Image(f'pic\{get_suit(id)}\{get_name(id)}.png', (CARD_WIDTH, CARD_HEIGHT), (250, 720-150))
            self.handcards_images[id] = img

        self.update_handcard_rect()
        pass


    def run(self):
        self.handcards_to_images()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for index in self.handcards:
                        self.handcards_images[index].select_move(event)
                elif event.type == pygame.MOUSEMOTION:
                    for index in self.handcards:
                        self.handcards_images[index].select_move(event)
                elif event.type == pygame.MOUSEBUTTONUP:
                    for index in self.handcards:
                        self.handcards_images[index].select_move(event)
            self.screen.fill((0,0,0))
            
            for i in self.handcards:
                self.handcards_images[i].draw(self.screen)
                # print()
            
            self.Clock.tick(60)
            pygame.display.update()





game = Game()
game.run()