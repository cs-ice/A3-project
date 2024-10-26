import pygame

class Button():
    def __init__(self, pos, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))       # 按钮文字
        self.rect = self.image.get_rect()                                   # 获取矩形
        self.rect.topleft = pos                                             # 初始化 按钮矩形位置
        self.clicked = False                                                # 按钮是否被点击
        self.able = True                                                    # 按钮是否可用
        

    def draw(self, surface):
        action = False
        bk = pygame.draw.rect(surface, (255, 255, 255), (self.rect.x, self.rect.y, self.image.get_width(), self.image.get_height()), 3)
        if bk.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(surface, (0, 0, 255), (self.rect.x, self.rect.y, self.image.get_width(), self.image.get_height()))
            # surface.blit(self.image, (self.rect.x, self.rect.y))
        else:
            pygame.draw.rect(surface, (0, 0, 0), (self.rect.x, self.rect.y, self.image.get_width(), self.image.get_height()), 1) 
        
        # mouse position
        pos = pygame.mouse.get_pos()

        # 点击判定

        if bk.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                pygame.draw.rect(surface, (0, 255, 0), (self.rect.x, self.rect.y, self.image.get_width(), self.image.get_height())) 
                self.clicked = True
                action = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False


        surface.blit(self.image, (self.rect.x, self.rect.y))

        
        
        return action

