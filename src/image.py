import pygame


class Image(pygame.sprite.Sprite):
    def __init__(self, path, size, pos):
        super().__init__()
        self.path = path                                            # 图片路径
        self.pos = list(pos)                                        # 图片位置
        
        self.start_pos = self.pos
        self.end_pos = self.pos
        self.is_moving = False
        self.start_time = pygame.time.get_ticks()


        self.size = size
        self.image = pygame.image.load(self.path)                   # 加载图片                                                               # 图片大小元组
        self.image = pygame.transform.scale(self.image, self.size)  # 转换大小
        self.rect = self.image.get_rect(topleft = pos)              # 获取图片矩形 图片移动就是移动矩形
        # self.rect.x, self.rect.y = pos                            # 改变矩形位置到目标pos
        self.pre_selected = False                                   # 预-选中
        self.is_selected = False                                    # 该图片是否被选中  
       

    
    def set_end_pos(self, end_pos):                                 # 设置终点 与move to搭配
        self.end_pos = end_pos
        self.start_time = pygame.time.get_ticks()
        self.is_moving  = True


    def set_rect(self, x, y, width, height):                        # 重新设定矩形 并更新位置
        self.rect.width = width
        self.rect.height = height
        self.set_end_pos((x, y))


    def move_to(self):                                              # 平移到指定坐标
        if not self.is_moving:
            return

        elapsed_time = pygame.time.get_ticks() - self.start_time    # 流逝的时间
        
        if (elapsed_time) >= 1500:                                  # 在1秒内完成移动 冗余
            self.rect.topleft = self.end_pos                        # 超时直接设置 就是快准狠
            self.is_moving = False
            return

        start_pos = pygame.Vector2(self.rect.topleft)
        end_pos = pygame.Vector2(self.end_pos)
        #print('start pos:', start_pos)
        #print('end pos:', end_pos)
        #print(elapsed_time)
        if start_pos == end_pos:
            #print('美国')
            return
        #print('过了')
        direction = end_pos - start_pos                             # 末减初
        distance = direction.length()                               # 速度越来越小了 而不是固定 所以有问题但不大
        speed = distance / 1                                        # 1s 这里写法上不太合适但是运行正常就不想改了
        displacement = direction.normalize()                        # 单位向量
        curr_pos = start_pos + displacement * (speed * elapsed_time / 1000)

        self.rect.topleft = (curr_pos.x, curr_pos.y)


    def select_move(self, event):
        print(event)
        if self.rect.collidepoint(event.pos):                  # 鼠标与牌重合 且牌没被选中 且按下按键 且按键是左键 牌才会升起 

            if event.type == pygame.MOUSEMOTION and event.buttons[0] == 1:
                self.pre_selected = True
                return  

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.pre_selected = True
                return           
      
            """ if event.type == pygame.MOUSEBUTTONDOWN and self.is_selected == True: # 按下按键且牌已被选中 那么取消选中并且移动会原来位置
                self.set_end_pos((self.end_pos[0], self.end_pos[1] + 20))
                self.is_selected = False
                return """
        
        if event.type == pygame.MOUSEBUTTONUP and self.pre_selected == True: # 松开鼠标 且已预选
            self.is_selected = not self.is_selected                      # 翻转选中状态
            if self.is_selected:
                self.set_end_pos((self.end_pos[0], self.end_pos[1] - 20))
            else:
                self.set_end_pos((self.end_pos[0], self.end_pos[1] + 20))  
            self.pre_selected = False
            return
        
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_selected == True and event.button == 3: # 按下右按键且牌已被选中 那么取消选中并且移动会原来位置
                self.set_end_pos((self.end_pos[0], self.end_pos[1] + 20))
                self.is_selected = False
                return

    
    def update(self):
        self.move_to()

 
    def draw(self, screen):
        self.update()
        screen.blit(self.image, self.rect)


    

