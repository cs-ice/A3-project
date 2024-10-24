'''
Poker类:
继承Image类, 以实现画出图形

类属性：1.Poker.id               即这张牌最重要的识别
        2.Poker.is_selected     该牌是否被选中

'''
import image
class Poker(image.Image):
    def __init__(self, path, size, pos, id):
        super().__init__(path, size, pos)
        self.id = id
        self.is_selected = False
        