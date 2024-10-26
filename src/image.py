import pygame


class Image(pygame.sprite.Sprite):
    def __init__(self, path, size, pos):
        super().__init__()
        self.path = path                                            # 图片路径
        self.pos = list(pos)                                        # 图片位置
        self.size = size
        self.image = pygame.image.load(self.path)                   # 加载图片                                                               # 图片大小元组
        self.image = pygame.transform.scale(self.image, self.size)  # 转换大小
        self.rect = self.image.get_rect(topleft = pos)                           # 获取图片矩形 图片移动就是移动矩形
        # self.rect.x, self.rect.y = pos                              # 改变矩形位置到目标pos
        self.is_selected = False                                    # 该图片是否被选中  
        self.start_time = pygame.time.get_ticks()

    def get_relative_position(self, x, y, SCREEN_WIDTH ,SCREEN_HEIGHT, surface):  
        # print((x / SCREEN_WIDTH) * surface.get_width())              # x, y指的是占据到哪个位置
        return (x / SCREEN_WIDTH) * surface.get_width() , (y / SCREEN_HEIGHT) * surface.get_height()


    def update(self):
        if pygame.time.get_ticks() - self.start_time >= 5000:       # 五秒钟消失
            self.kill()           
        

    def doUP(self):
        self.pos[1] -= 15                                           # y坐标-1 图片向上移动
        self.rect.x, self.rect.y = self.pos
    
    def doDown(self):
        self.pos[1] += 15                                           # y坐标-1 图片向上移动
        self.rect.x, self.rect.y = self.pos

    
    def draw(self, ds):                                             # ds 即display 画布的意思 画在这个画布上
        self.rect.x,self.rect.y = self.get_relative_position(self.rect.x, self.rect.y, 1280, 800, ds)
        ds.blit(self.image, self.rect)
    
    def move(self):                                                 # 简易模拟选牌上下移动
        if self.is_selected:
            self.doDown()
            self.is_selected = False
        else:
            self.doUP()
            self.is_selected = True
    
    def get_ID(self):                                               # 返回ID
        return self.id


    def rect_resize(self):                                          # 重新计算矩形 因为牌会重叠
        pass

    
    