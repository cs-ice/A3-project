import pygame
import string

class InputBox:
    def __init__(self, surface, left, top, width, height, font):
        self.surface = surface
        self.font = font
        self.rect = pygame.Rect(left, top, width, height)
        self.list = []
        # 是否激活
        self.active = False
        # 是否绘制光标
        self.cursor = True
        # 光标绘制计数器
        self.count = 0
        # 删除状态
        self.delete = False



    def draw(self):
        # 画框
        pygame.draw.rect(self.surface, (0,0,0), self.rect, 1)
        # 投放文字
        text_pic = self.font.render(''.join(self.list), True, (0,0,0))
        self.surface.blit(text_pic, (self.rect.x+5, self.rect.y+5))
        # 更新光标计数器
        self.count += 1
        if self.count == 20:
            self.count = 0
            self.cursor = not self.cursor

        # 绘制光标

        if self.active and self.cursor:
            text_pic_rect = text_pic.get_rect()
            x = self.rect.x + 5 + text_pic_rect.width
            pygame.draw.line(self.surface, (0,0,0), (x, self.rect.y + 5), (x,self.rect.y+self.rect.height - 5), 1)


        # 删除状态
        """ if self.delete and self.list:
            self.list.pop()
            for i in range(60):
                pass """
            

    def get_text(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False

        elif self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE and self.list:
                    # self.delete = True
                    self.list.pop()
                """ 
                elif event.unicode in string.ascii_letters or \
                    event.unicode in '0123456789_':                 # 仅支持字母数字
                    self.list.append(event.unicode) """
            elif event.type == pygame.TEXTINPUT:
                for i in list(event.text):                          # 拆成字符进入列表
                    self.list.append(i)
                

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE:
                    self.delete = False


    def return_text(self):
        return ''.join(self.list)







