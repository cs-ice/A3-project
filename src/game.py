import os
os.environ["SDL_IME_SHOW_UI"] = "1"    # 显示输入候选框 0是False 1是True
import pygame
from image import *
from client import *
from player import Player
from button import Button
from inputbox import InputBox
import sys


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



class Game(Client):                                 # 继承client
    def __init__(self):
        super().__init__()

        pygame.init()
        pygame.font.init()                          # 加载字体渲染
        pygame.display.set_caption('A3')
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.font = pygame.font.SysFont('华文楷体', 20)
        self.Clock = pygame.time.Clock()
        self.all_card_images = {}                  # 整幅牌的图形 初始化
        self.player_positions = [(1280-66-20, 250), (590, 20), (20, 250), (590, 620)] # 右上左下的玩家位置
        # 关系到位置分配 用一个remove一个

        self.handcards = [x+9 for x in range(9)]                                     # 手牌的ID列表
        self.handcards_images = {}                 # 手牌的图像字典   格式{card_ID： Image}
        self.handcards_length = 0                  # 手牌长度 用于检测手牌长度变化 若变化就更新手牌绘制

        self.deskcards = []
        self.deskcards_images = {}
        self.deskcards_sprite_groups = {}                  # 字典 {PLAYERID: SpriteGroup}


        self.myid = -1
        self.order = []                                     # 本地化的顺序 自己是第一号元素 [myid, rightid, upwardid, leftid]
        self.order_id_dict = []                             # {0:myid, 1:.....}


        self.player_pool = {}                               # 玩家池 {id: Player}

    '''
    若手牌数量发生变化  更新手牌的位置
    '''
    def update_handcard_rect(self):
        curr_handcards_len = len(self.handcards)
        #print(self.handcards_length)
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

    '''
    将自己的手牌发送至牌桌 
    '''
    def send_to_desk(self):                         # 应该是无需实时更新的 只需要在出牌的时候更新就行
        for card_id, image in self.handcards_images.items():
            if image.on_desk:
                image.set_end_pos((440, 275))
                self.deskcards_images[card_id] = image  # 即把on_desk的牌移动到这个字典里
        # 遍历过程中删除可能造成意想不到的错误 所以下面单独删除

        for key in self.deskcards_images.keys():        # 遍历桌上字典的键
            self.handcards.remove(key)
            del self.handcards_images[key]




    def update_deskcard_rect(self):                         # 负责更新牌桌 精灵的矩形
        # 目前想法 每接收一个playerID发来的牌 就只更新该ID的就行
        # 所以 需要接受一组牌的ID列表 接受一个玩家ID 知道该ID 还需要根据ID获得该ID的order
        
        # 五张牌占400 最后一张100 所以只有300可分配

        length = len(card_lst)      # 根据牌的长度操作

        if order == 0:       # 即自己 下方
            if length == 1:
                image = self.all_card_images[card_id]
                image.set_end_pos(590, 275)
                # 将这张image加入到 order为0的group即可
            elif length == 2:
                image1 = self.all_card_images[card_id]
                image2 = self.all_card_images[card_id]
                image1.set_end_pos(540, 275)
                image2.set_end_pos(640, 275)
                # 同理加入即可
            elif length == 3:
                image1 = self.all_card_images[card_id]
                image2 = self.all_card_images[card_id]
                image3 = self.all_card_images[card_id]
                image1.set_end_pos(490, 275)
                image2.set_end_pos(590, 275)
                image3.set_end_pos(690, 275)

            elif length == 4:
                pass
            elif length == 5:
                pass
               
                
        elif order == 1:     # 右方
            pass
        elif order == 2:     # 上方
            pass
        elif order == 3:     # 左方
            pass

        
        # 调用该方法 新建一个新玩家 并把该玩家加入 玩家池字典中 self.player_pool
        # 适用于准备界面
    def create_player(self, newplayer_id, newplayer_name):
        if len(self.player_positions) == 0:
            print('位置列表已空, 请检查错误\n')
            return

        newplayer = Player()
                                                                    # 根据玩家的本地化order来设置位置
        if newplayer_id == self.player_id:                          # 若新建的玩家是自己 坐下面
            newplayer.set_player_pos(self.player_positions.pop()) 
        else:
                                                                    # 直接坐列表第一个位置即可
            newplayer.set_player_pos(self.player_positions.pop(0))

        newplayer.set_player_nickname(newplayer_name)               # 设置名字
        self.player_pool[newplayer_id] = newplayer


        # 准备界面
    def waiting_scene(self):
        WAIT_bg = Image('pic\waitbg.jpg', (1280,720),(0,0))                     # 加载等待背景图片
        waiting = True
        inputBox_room = InputBox(self.screen, 500, 400, 300, 40, self.font)     # 房间号 昵称 输入框
        inputBox_name = InputBox(self.screen, 500, 320, 300, 40, self.font)

        font = pygame.font.SysFont('华文楷体', 30)
        text_room = font.render('房间号:', True, (255, 255, 255))           # 文字渲染
        text_name = font.render('昵称:', True, (255, 255, 255))
        text_login = font.render('快速开始', True, (255, 255, 255))

        button_login = Button((580, 500), text_login, 1)                        # 快速开始 按钮

        while waiting:
            for event in pygame.event.get():
                
                inputBox_room.get_text(event)                                   # 文本框在读取事件获得输入
                inputBox_name.get_text(event)
                if event.type == pygame.KEYDOWN:
                    print(event.unicode)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pass
                elif event.type == pygame.MOUSEMOTION:
                    pass
                elif event.type == pygame.MOUSEBUTTONUP:
                    pass
                
                
            
            WAIT_bg.draw(self.screen)                                           # 绘制背景

            self.screen.blit(text_room, (400, 400))                             # 绘制文字
            self.screen.blit(text_name, (430, 320))
            inputBox_room.draw()                                                # 绘制文本框
            inputBox_name.draw()
            if button_login.draw(self.screen):                                  # 绘制按钮并读取按钮输入
                waiting = False
                return inputBox_name.return_text(), inputBox_room.return_text() # 返回输入框内容
            self.Clock.tick(60)

            pygame.display.update()

    def ready_scene(self):
        ready = True
        READY_bg = Image('pic\gamebg.png', (1280,720),(0,0))
        font = pygame.font.SysFont('华文楷体', 40)
        text_ready = font.render('准备', True, (255,255,255))
        button_ready = Button((600, 500),text_ready , 1) 

        while ready:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pass
                elif event.type == pygame.MOUSEMOTION:
                    pass
                elif event.type == pygame.MOUSEBUTTONUP:
                    pass
            READY_bg.draw(self.screen)
            if button_ready.draw(self.screen):
                pass

            pygame.display.update()




    def run(self):
        i = 0
        while True:
            name, room = self.waiting_scene()
            room_id = int(room)
            if self.sed_room_and_name(room_id, name):
                break
            i+=1


        self.ready_scene()



        self.handcards_to_images()
        player1 = Player((20, 250))
        player2 = Player((1280-66-20, 250))
        player3 = Player((590, 20))
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # self.handcards_images[10].on_desk = True
                    self.send_to_desk()
                    for index in self.handcards:
                        self.handcards_images[index].select_move(event)
                    self.update_handcard_rect()
                    
                elif event.type == pygame.MOUSEMOTION:
                    self.handcards_images[11].set_end_pos(event.pos)
                    # print(event.pos)
                    for index in self.handcards:
                        self.handcards_images[index].select_move(event)
                elif event.type == pygame.MOUSEBUTTONUP:
                    for index in self.handcards:
                        self.handcards_images[index].select_move(event)
            self.screen.fill((0,0,0))
            player1.draw(self.screen)
            player2.draw(self.screen)
            player3.draw(self.screen)
            for i in self.handcards:
                self.handcards_images[i].draw(self.screen)
                # print()
            for i in self.deskcards_images:
                self.deskcards_images[i].draw(self.screen)
            
            
                # print(i)
                # print()
            self.Clock.tick()
            pygame.display.update()





game = Game()
game.run()