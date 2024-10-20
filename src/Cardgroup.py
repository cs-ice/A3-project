from Card import *
from macro import *
@constant
def INVALID():
    return -1
@constant
def SINGLE():
    return 0
@constant
def DOUBLE():
    return 1
@constant
def THREE():
    return 2
@constant
def SEQ():
    return 3
@constant    
def UNISUIT():
    return 4
@constant
def THREETWO():
    return 5
@constant
def FOURONE():
    return 6
@constant
def UNISEQ():
    return 7


class Cardgroup:
    def __init__(self):
        self.cards = []                         # 储存Card类卡牌
        self.cardpoints = []
        self.type =  INVALID                           # 0无效 1为单 2为对 3为三 5为
        pass

    def add_card(self, card):                   # 往卡组添加牌，并update类型
        self.cards.append(card)
        self.judgeType()                        # update

    def remove_card(self, card):                # 移除
        if(card in self.cards):
            self.cards.remove(card)
            self.judgeType()
    
    def update_cardpoints(self, point):
        pass


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