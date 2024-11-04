import pygame

pygame.init()
screen = pygame.display.set_mode((1280,720))


class Player:
    def __init__(self, pos):
        pygame.font.init()
        # 图片区
        self.image = pygame.image.load('pic\CardBack.png')
        self.pos = list(pos)
        self.rect = self.image.get_rect(topleft=(self.pos))

        # 牌数量区
        self.font = pygame.font.SysFont('华文楷体', 30)
        self.number_text = self.font.render('', True, (255, 0, 0))
        self.number_rect = pygame.Rect(self.rect.left,self.rect.top,self.rect.width,self.rect.height)

        # 昵称区
        self.nickname_text = self.font.render('Nickname', True, (255, 255, 255))
        
        
        
        # 设置剩余手牌数
    def set_card_numbers(self, num):
        self.number_text = self.font.render(f'{num}', True, (255, 0, 0))
        if num < 10:
            self.number_rect.x = self.rect.x + 25           # 个位数的位置向右移动一点
        else:
            self.number_rect.x = self.rect.x + 17           # 两位数也要右移

        # 设置昵称
    def set_player_nickname(self, nickname):
        self.nickname_text = self.font.render(str(nickname), True, (255, 255, 255))


    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.number_text, self.number_rect)
        screen.blit(self.nickname_text,(self.rect.x, self.rect.y+88))


# j = 19

# p1 = Player((100,200))
# while 1:
#     for i in pygame.event.get():
#         if i.type == pygame.QUIT:
#             pygame.quit()
#         elif i.type == pygame.MOUSEBUTTONDOWN:
#             p1.set_card_numbers(j)
#             p1.set_player_nickname('张三')
#             p1.rect.x = 1000
#             j -= 1

#     screen.fill((0,0,0))
#     p1.draw(screen)
#     pygame.display.update()



