from Card import *
INVALID = -1       # 无效
SINGLE = 0         # 单张
DOUBLE = 1         # 对子
THREE = 2          # 三张
SEQ = 3            # 顺子
UNISUIT = 4        # 同花
THREETWO = 5       # 三带二
FOURONE = 6        # 四带一
UNISEQ = 7         # 同花顺



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

    def sort(self):                             # 排序 一般用于手牌 依据card的num降序排序
        self.cards.sort(key=lambda x: x.num, reverse=True)

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
            i.show_suit()
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