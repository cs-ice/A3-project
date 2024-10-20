from Card import *
from macro import *
@constant
def INVALID():                          # 无效类型标识常数
    return -1
@constant
def SINGLE():                           # 单牌
    return 0
@constant
def DOUBLE():                           # 对子
    return 1
@constant
def THREE():                            # 三个
    return 2
@constant
def SEQ():                              # 顺子
    return 3
@constant    
def UNISUIT():                          # 同花色
    return 4
@constant
def THREETWO():                         # 三带二
    return 5
@constant
def FOURONE():                          # 四带一
    return 6
@constant
def UNISEQ():                           # 同花顺
    return 7


class Cardgroup:
    def __init__(self):
        self.cards = []                         # 储存Card类卡牌
        self.cardpoints = []                    # 储存点数, 为了方便后续判断type
        self.type =  INVALID                           # -1无效 0为单 1为对 2为三 etc.
        pass

    def add_card(self, card):                   # 往卡组添加牌，并update类型
        self.cards.append(card)
        self.judgeType()                        # update
        self.update_cardpoints(card.point)

    def remove_card(self, card):                # 移除牌 并update
        if(card in self.cards):
            self.cards.remove(card)
            self.judgeType()
    
    def update_cardpoints(self, point):
        self.cardpoints.append(point)
        self.cardpoints.sort()                  # 按顺序排序点数, 方便操作


    def judgeType(self):                        # 判断类型
        length = len(self.cards)

        if(length == 1):
            self.type = SINGLE
        elif(length == 2):
            if(self.cards[0].point == self.cards[1].point):
                self.type = DOUBLE
            else:
                self.type = INVALID
        elif(length == 3):
            if((self.cards[0].point == self.cards[1].point) and (self.cards[0].point == self.cards[2].point)):
                self.type = THREE
            else:
                self.type = INVALID
        elif(length == 4):
            self.type = INVALID
        elif(length == 5):
            pass
    


        

    
    
    
    def show(self):
        for i in self.cards:
            i.show_color()
            i.isJQK()


c1 = Card(10)
c2 = Card(23)
c3 = Card(12)

group = Cardgroup()

group.add_card(c1)
group.add_card(c2)
print(group.type)
group.add_card(c3)
print(group.type)
group.show()