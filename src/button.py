import image

class Button(image.Image):
    def __init__(self, path, size, pos):
        super().__init__(path, size, pos)
        self.is_press = False
        self.text = None                                        # 渲染后的字体对象

    def font_draw(self):
        self.image.blit(self.text, self.rect)
