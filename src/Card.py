class Card:
    def __init__(self, num):
        self.num = num
        self.suit = self.get_suit()         # 根据编号初始化花色和点数
        self.point = self.get_point()


    def get_suit(self):
        return self.num // 13           # 3spade, 2heart, 1club, 0diamond

    def get_point(self):
        return self.num % 13            # 返回0是卡牌4， 返回12是卡牌3

    def isJQK(self):                    # 判断是不是JQKA23等特殊值
        if(self.point == 7):
            print('J')
        elif(self.point == 8):
            print('Q')
        elif(self.point == 9):
            print('K')
        elif(self.point == 10):
            print('A')
        elif(self.point == 11):
            print('2')
        elif(self.point == 12):
            print('3')
    
    def show_suit(self):               # 仅展示花色
        if(self.suit == 3):
            print('Spade')
        elif(self.suit == 2):
            print('Heart')
        elif(self.suit == 1):
            print('Club')
        elif(self.suit == 0):
            print('Diamond')

    

