
INVALID = -1         # 无效
SINGLE = 0           # 单张
DOUBLE = 1           # 对子
THREE = 2            # 三张
STRAIGHT = 3         # 顺子
FLUSH = 4            # 同花
THREETWO = 5         # 三带二
FOURONE = 6          # 四带一
FLUSHSTRAIGHT = 7    # 同花顺


def get_point(card_id): 
    return card_id % 13            # 返回0是卡牌4， 返回12是卡牌3

def get_suit(card_id):
    return card_id // 13           # 3spade, 2heart, 1club, 0diamond

def show(card_id):                  # 翻译ID成牌
    point = get_point(card_id)
    s = get_suit(card_id)
    if(s == 0):
        print('♦', end="")
    elif(s == 1):
        print('♣', end="")
    elif(s == 2):
        print('♥', end="")
    elif(s == 3):
        print('♠', end="")
    if(point == 7):
        print('J', end=" ")
    elif(point == 8):
        print('Q', end=" ")
    elif(point == 9):
        print('K', end=" ")
    elif(point == 10):
        print('A', end=" ")
    elif(point == 11):
        print('2', end=" ")
    elif(point == 12):
        print('3', end=" ")
    else:
        print(point+4, end=" ")
    
'''
卡组类需要实现的功能
1.储存一组牌，通过储存牌的ID列表实现
2.通过ID获取牌的点数与花色
3.能够添加，删除牌。同时判断此时的牌组类型
4.若是有效类型，计算它的value

'''

class Cardgroup:
    def __init__(self):
        self.cards = []                         # 储存卡牌ID, 整型
        self.type =  INVALID                           # -1无效 0为单 1为对 2为三 etc.
        self.deter_ID = -1                      # 牌组大小的决定性手牌ID
        self.value = -1                         # 对于三张和五张牌的大小评估，同type才比较
        pass
    
    def add_card(self, card_id):                   # 往卡组添加牌，并update类型
        self.cards.append(card_id)
        # self.judgeType()                        # update
        # self.update_cardpoints(card.point)

    def sort(self):                             # 排序 一般用于手牌 依据card的num降序排序
        self.cards.sort(key=lambda x: x.num, reverse=True)

    def remove_card(self, card):                # 移除牌 并update
        if(card in self.cards):
            self.cards.remove(card)
            self.judgeType()
    

        '''
        不接受参数，使用到self.cards列表，不改变列表
        返回值：布尔类型
        作用：判断self.cards储存的是否是顺子
        '''
    def isSTRAIGHT(self):   
        temp_points = []                            # 临时列表 储存一组点数
        maxpoint_id = -1                        # 初始化为第一张牌的id, 记录最大点数对应的ID，以求它的花色
        max_point = -1                          # 最大点数, 并初始化
        current_point = -1                          # 这两者都是临时变量，分别是上一个和当前点数
        for id in self.cards:
            current_point = get_point(id) 
            if(current_point == 11):                 # 11是卡牌2的id, 顺子不包含卡牌2
                return False
            elif(current_point == 12):              # !!! 3开头的顺子是最小的, 所以这里处理为0
                current_point = 0
            else:
                current_point += 1                  # 因为卡牌3在顺子中为0, 所以卡牌4等需要+1
            
            temp_points.append(current_point)
            if(current_point > max_point):         # 如果当前点数较大，则保存ID
                maxpoint_id = id
                max_point = current_point

                

        temp_points.sort()                      # 升序排序

        for i in range(4):                      # 长度为5，最大索引为4，即3+1
            if(temp_points[i+1] == temp_points[i] + 1): # 后一位比前一位大一
                continue
            else:
                return False                            # 否则就不是顺子

        self.deter_ID = maxpoint_id                     # 顺子的决定性因素是点数最大的那张牌
        return True
        
    def isFLUSH(self):
        prev_suit = get_suit(self.cards[0])         # 先初始化为第一张牌的花色
        current_suit = get_suit(self.cards[0])      
        maxpoint_id = 0                             # 记录最大点数对应的ID，以求它的花色
        prev_point = -1
        current_point = -1                          # 这两者都是临时变量，分别是上一个和当前点数
        for id in self.cards:
            current_suit = get_suit(id)
            if(current_suit != prev_suit):
                return False                        # 当前花色与上一张不相等，False

            current_point = get_point(id)
            if(current_point > prev_point):         # 如果当前点数较大，则保存ID
                maxpoint_id = id
            prev_point = current_point              # 将上一个点数更新为当前点数
            prev_suit = current_suit                # 将上一个花色更新为当前花色

        self.deter_ID = maxpoint_id                 # 同花决定于 花色，点数
        return True

    def isTHREETWO(self):
        element_count = {}                          # 创建一个字典，点数即字典的key
        for id in self.cards:
            elem = get_point(id)                    # 元素即点数
            if elem in element_count:               # 若该元素已存在key，则递增1
                element_count[elem] += 1            
            else:
                element_count[elem] = 1             # 若否，创建键值对
            if element_count[elem] == 3:            # 重复三次，说明是三带对
                self.deter_ID = elem
                return True

        return False        
        
    def isFOURONE(self):
        element_count = {}                          # 参考三带对，CV过来的
        for id in self.cards:
            elem = get_point(id)                    # 元素即点数
            if elem in element_count:               # 若该元素已存在key，则递增1
                element_count[elem] += 1            
            else:
                element_count[elem] = 1             # 
            if element_count[elem] == 4:            # 重复4次，说明是四代一
                self.deter_ID = elem
                return True

        return False

        '''
        judgeType()
        功能：判断当前牌组(self.cards)的类型
        参数: 无, 需要使用self.cards, 不会改变列表
        返回值: 无, 但是会改变self.type的值
        实现: 先判断长度, 在判具体类型
        '''
    def judgeType(self):                        # 判断类型
        length = len(self.cards)

        if(length == 1):
            self.type = SINGLE
        elif(length == 2):
            p1, p2 = get_point(self.cards[0]), get_point(self.cards[1])       # p1p2临时储存点数
            if(p1 == p2):
                self.type = DOUBLE
            else:
                self.type = INVALID
        elif(length == 3):
            p1, p2 = get_point(self.cards[0]), get_point(self.cards[1])
            p3 = get_point(self.cards[2])
            if((p1 == p2) and (p1 == p3)):
                self.type = THREE
            else:
                self.type = INVALID
        elif(length == 4):
            self.type = INVALID
        elif(length == 5):
            if(self.isSTRAIGHT() and self.isFLUSH()):   # 先判同花顺，因为它和顺子，同花判断重合
                self.type = FLUSHSTRAIGHT
            elif (self.isSTRAIGHT()):                     # 判断顺子
                self.type = STRAIGHT
            elif (self.isFLUSH()):                      # 判断同花
                self.type = FLUSH
            elif(self.isFOURONE()):                     # 先判四带一，因为和三带对判断重合
                self.type = FOURONE
            elif(self.isTHREETWO()):                    # 判三带一
                self.type = THREETWO
            else:
                self.type = INVALID
    '''
    calcValue()
    作用: 在已知type后, 计算牌组的分数
    参数: 无, 需要用到self.type, self.deter_ID
    返回值: 无, 通过self.value传值
    '''
    def calcValue(self):
        sum = 0
        point = get_point(self.deter_ID)
        suit = get_suit(self.deter_ID)
        if(self.type == INVALID):
            self.value = -1
        elif(self.type == SINGLE):
            pass                                # 
        elif(self.type == DOUBLE):
            pass
        elif(self.type == THREE):
            pass
        elif(self.type == STRAIGHT):
            pass

        elif(self.type == FLUSH):           # 从方片到梅花, 分数加13, 方片9为最低分1分
            while (suit > 0):
                sum += 13
                suit -= 1
            while point >= 5:                 # point 5 即 卡牌9
                sum += 1
                point -= 1

        elif(self.type == THREETWO):        # 三带一只看点数, 所以分数即是点数+1, 规定最低分是1
            sum = get_point(self.deter_ID) + 1
        elif(self.type == FOURONE):         # 四带一同理
            sum = get_point(self.deter_ID) + 1
        elif(self.type == FLUSHSTRAIGHT):   
            pass
        
        print(sum)
    def show(self):
        pass



group = Cardgroup()
group.add_card(45-13)
group.add_card(46)
group.add_card(47)
group.add_card(48)
group.add_card(49)
group.judgeType()
if group.type == 3:
    print('顺子')
show(group.deter_ID)
group.calcValue()
for i in range(5):
    print(get_point(group.cards[i])+4, end=' ')