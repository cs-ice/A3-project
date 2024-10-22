'''
===========================================DOCUMENTATION====================================================

Cardgroup类
类属性: 1. Cardgroup.cards     一个int列表, 保存一组牌
        2.Cardgroup.type      该卡组的类型
        3.Cardgroup.deter_ID  决定性ID, 主要通过它比较牌组的大小
        4.Cardgroup.value     牌组分数, 只有在类型相同时, 直接通过它比较牌组的大小

类方法:  1.Cardgroup.add_card(card_id)    
        该方法需要一个int类型参数, 参数即卡牌的ID
        该方法往卡组(Cardgroup)添加一张卡牌, 并更新卡组类型(Cardgroup.type)以及计算分数(Cardgroup.value)
       
        2.Cardgroup.remove_card(card_id)
        该方法需要一个int类型参数, 参数即卡牌的ID
        该方法将卡组(Cardgroup)移除一张特定卡牌, 并更新卡组类型(Cardgroup.type)以及计算分数(Cardgroup.value)
    
        3.Cardgroup.judgeType()
        该方法无需参数 直接根据当前卡组(Cardgroup.cards)判断出卡组类型(Cardgroup.type), 结果直接保存到Cardgroup.type
        同时, 该方法也传递出当前卡组的决定性因素, 并保存在Cardgroup.deter_ID中

        4.Cardgroup.calcValue()
        该方法无需参数, 根据当前卡组的类型(Cardgroup.type)和卡组的决定性因素(Cardgroup.deter_ID)计算出卡组的分数, 
        并保存在Cardgroup.value中.

        5.Cardgroup.showcard()
        该方法在控制台展示保存在卡组中的牌及类型

        6.各种判断牌类型的方法


全局函数:
        1.get_point(card_id)
        需要一个牌的ID, 返回该牌的点数
        
        2.get_suit(card_id)
        需要一个牌的ID, 返回该牌的花色

        3.show(card_id)
        需要一个牌的ID, 在控制台打印该牌


'''

INVALID = -1         # 无效
SINGLE = 0           # 单张
DOUBLE = 1           # 对子
THREE = 2            # 三张
FOUR = 3             # 四张
STRAIGHT = 4         # 顺子
FLUSH = 5            # 同花
THREETWO = 6         # 三带二
FOURONE = 7          # 四带一
FLUSHSTRAIGHT = 8    # 同花顺


def get_point(card_id): 
    return card_id // 4            # 返回0是卡牌4， 返回12是卡牌3

def get_suit(card_id):
    return card_id %  4           # 3spade, 2heart, 1club, 0diamond

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
1.储存一组牌 通过储存牌的ID列表实现
2.通过ID获取牌的点数与花色
3.能够添加 删除牌。同时判断此时的牌组类型
4.若是有效类型 计算它的value

'''

class Cardgroup:
    def __init__(self):
        self.cards = []                         # 储存卡牌ID, 整型
        self.type =  INVALID                    # -1无效 0为单 1为对 2为三 etc.
        self.deter_ID = -1                      # 牌组大小的决定性手牌ID
        self.value = -1                         # 对于三张和五张牌的大小评估，同type才比较
        pass
    
    def add_card(self, card_id):                   # 往卡组添加牌，并update类型
        self.cards.append(card_id)
        self.judgeType()                           # update
        self.calcValue()                           # 计算VALUE


    def sort(self):                                # 排序 一般用于手牌 依据card的num降序排序
        self.cards.sort(reverse=True)

    def remove_card(self, card):                   # 移除牌 并update
        if(card in self.cards):
            self.cards.remove(card)
            self.judgeType()
            self.calcValue()
    

        '''
        不接受参数 使用到self.cards列表 不改变列表
        返回值：布尔类型
        作用 判断self.cards储存的是否是顺子
        '''
    def isSTRAIGHT(self):   
        temp_points = []                            # 临时列表 储存一组点数
        maxpoint_id = -1                            # 初始化为第一张牌的id, 记录最大点数对应的ID，以求它的花色
        max_point = -1                              # 最大点数, 并初始化
        current_point = -1                          # 这两者都是临时变量，分别是上一个和当前点数
        for id in self.cards:
            current_point = get_point(id) 
            if(current_point == 11):                 # 11是卡牌2的id, 顺子不包含卡牌2
                return False
            elif(current_point == 12):               # !!! 3开头的顺子是最小的, 所以这里处理为0
                current_point = 0
            else:
                current_point += 1                   # 因为卡牌3在顺子中为0, 所以卡牌4等需要+1
            
            temp_points.append(current_point)
            if(current_point > max_point):           # 如果当前点数较大，则保存ID
                maxpoint_id = id
                max_point = current_point

        temp_points.sort()                              # 升序排序

        for i in range(4):                              # 长度为5，最大索引为4，即3+1
            if(temp_points[i+1] == temp_points[i] + 1): # 后一位比前一位大一，就是顺子
                continue
            else:
                return False                            # 否则就不是顺子

        self.deter_ID = maxpoint_id                     # 顺子的决定性因素是点数最大的那张牌
        return True
        
    def isFLUSH(self):
        prev_suit = get_suit(self.cards[0])         # 先初始化为第一张牌的花色
        current_suit = get_suit(self.cards[0])      
        maxpoint_id = -1                            # 记录最大点数对应的ID，以求它的花色
        prev_point = -1
        current_point = -1                          # 这两者都是临时变量，分别是上一个和当前点数
        for id in self.cards:
            current_suit = get_suit(id)
            if(current_suit != prev_suit):
                return False                        # 当前花色与上一张不相等，False

            current_point = get_point(id)
            if(current_point > prev_point):         # 如果当前点数较大，则保存ID
                maxpoint_id = id
                prev_point = current_point          # 将上一个点数更新为当前最大点数
            
            prev_suit = current_suit                # 将上一个花色更新为当前花色

        self.deter_ID = maxpoint_id                 # 同花决定于 花色，点数
        return True

    def isTHREETWO(self):
        element_count = {}                          # 创建一个字典，点数即字典的key
        key_lst = []                                # 保存key， 只有次数是3和2才TRUE
        for id in self.cards:
            elem = get_point(id)                    # 元素即点数
            if elem in element_count:               # 若该元素已存在key，则递增1
                element_count[elem] += 1            
            else:
                element_count[elem] = 1             # 若否，创建键值对
                key_lst.append(id)                  # 保存ID
        
        if(len(key_lst) != 2):                      # 点数超过两种，肯定不是三带对
            return False
        key1, key2 = get_point(key_lst[0]), get_point(key_lst[1])               # key变量是点数
        if (element_count[key1] == 3) and (element_count[key2] == 2):           # 点数重复三次，说明是三带对
            self.deter_ID = key_lst[0]                          
            return True
        elif (element_count[key1] == 2) and (element_count[key2] == 3):         # 重复三次，说明是三带对
            self.deter_ID = key_lst[1]                                          # 决定ID为出现三次的卡牌点数 只需要点数即可 不需要花色
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
                self.deter_ID = id                  # 决定ID 为重复四次那张牌 只需要点数即可 不需要花色
                return True

        return False

    '''
    judgeType()
    功能：判断当前牌组(self.cards)的类型, 同时获取决定性ID
    参数: 无, 需要使用self.cards, 不会改变列表
    返回值: 无, 但是会改变self.type, self.deter_ID的值
    实现: 先判断长度, 在判具体类型
    '''
    def judgeType(self):                                                    # 判断类型 同时取得决定性ID以算取value
        length = len(self.cards)
        self.type = INVALID
        self.deter_ID = -1                                                  # 每次判断前 先重置Type和deterID
        self.value = -1

        if(length == 1):
            self.type = SINGLE
            self.deter_ID = self.cards[0]
        elif(length == 2):
            p1, p2 = get_point(self.cards[0]), get_point(self.cards[1])     # p1p2临时储存点数
            if(p1 == p2):
                self.type = DOUBLE
                self.deter_ID = max(self.cards[0], self.cards[1])
            else:
                self.type = INVALID
        elif(length == 3):
            p1, p2 = get_point(self.cards[0]), get_point(self.cards[1])
            p3 = get_point(self.cards[2])
            if((p1 == p2) and (p1 == p3)):
                self.type = THREE
                self.deter_ID = self.cards[0]                               # 三张的决定性ID 由于不判花色 默认取第一张的ID
            else:
                self.type = INVALID
        elif(length == 4):
            temp = get_point(self.cards[0])
            for i in range(1, 4):
                if(get_point(self.cards[i]) != temp):
                    self.type = INVALID
                    return
            self.type = FOUR
            self.deter_ID = self.cards[0]                                   # 四张的决定性ID 由于不判花色 默认取第一张的ID
        elif(length == 5):
            '''
            注意 这里判断同花顺 必须先判同花 因为同花的决定ID是取大牌 而同花顺侧重尾号牌
            如黑桃34567 如果后判同花 决定ID是黑桃3 而正确ID是黑桃7

            注 决定ID已经在is__方法中取得
            '''
            if(self.isFLUSH() and self.isSTRAIGHT()):   # 先判同花顺，因为它和顺子，同花判断重合
                self.type = FLUSHSTRAIGHT
            elif (self.isSTRAIGHT()):                   # 判断顺子
                self.type = STRAIGHT
            elif (self.isFLUSH()):                      # 判断同花
                self.type = FLUSH
            elif(self.isFOURONE()):                     # 先判四带一，因为和三带对判断重合
                self.type = FOURONE
            elif(self.isTHREETWO()):                    # 判三带一
                self.type = THREETWO
            else:
                self.type = INVALID
        else:
            self.type = INVALID
    '''
    calcValue()
    作用: 在已知type后, 计算牌组的分数
    参数: 无, 需要用到self.type, self.deter_ID
    返回值: 无, 通过self.value传值
    一般用在judgeType()的后面
    '''
    def calcValue(self):                    # 为了代码的一致性，self.value是由scores赋值的 所以请修改scores
        scores = 0
        point = get_point(self.deter_ID)    # 分别获取决定ID的花色和点数
        suit = get_suit(self.deter_ID)
        if(self.type == INVALID):
            scores = -1                     # 无效类型 分数是-1
        elif(self.type == SINGLE):
            scores = self.deter_ID          # 单牌分数即ID
        elif(self.type == DOUBLE):
            scores = self.deter_ID          # 对子即取大的ID，因为大的ID对应大的花色
        elif(self.type == THREE):                                           
            scores = self.deter_ID          # 三张同理   
        elif(self.type == FOUR):            
            scores = self.deter_ID          # 四张同理
        elif(self.type == STRAIGHT):        
            scores = self.deter_ID          # 取决于deter_ID 那VALUE就是ID  

        elif(self.type == FLUSH):           # 从方片到梅花, 分数加13, 方片9为最低分1分
            while (suit > 0):
                scores += 13
                suit -= 1
            while point >= 5:               # point 5 即 卡牌9
                scores += 1
                point -= 1

        elif(self.type == THREETWO):        # 三带一只看点数, 所以分数即是点数+1, 规定最低分是1
            scores = get_point(self.deter_ID) + 1
        elif(self.type == FOURONE):         # 四带一同理
            scores = get_point(self.deter_ID) + 1
        elif(self.type == FLUSHSTRAIGHT):   # 同花顺和顺子的判断是一模一样的
            scores = self.deter_ID
        
        self.value = scores
        # print(scores)

    def showcard(self):
        if self.type == INVALID:
            print('INVALID')
        elif self.type == SINGLE:
            print('单牌')
        elif self.type == DOUBLE:
            print('对子')
        elif self.type == THREE:
            print('三张')
        elif self.type == FOUR:
            print('四张')
        elif self.type == STRAIGHT:
            print('顺子')        
        elif self.type == FLUSH:
            print('同花')
        elif self.type == FOURONE:
            print('四带一')
        elif self.type == THREETWO:
            print('三带对')
        elif self.type == FLUSHSTRAIGHT:
            print('同花顺')
        for i in self.cards:
            show(i)




""" 
while True:
    group = Cardgroup()
    i = int(input('输入几张牌？'))
    for _ in range(i):
        group.add_card(int(input()))
    group.judgeType()
    print("决定牌:", end="")
    show(group.deter_ID)
    print()
    group.calcValue()
    print('Value:', str(group.value))
    group.showcard()                            # 测试代码区 """
    # print()


group = Cardgroup()
while True:
    input_str = input("输入操作 (例如: 'add 0 3' 或 'remove 1 10' 或 'exit'): ").split()
    command = input_str[0]

    if command == 'add' and len(input_str) == 3:
        card_suit = int(input_str[1])
        card_point = int(input_str[2])
        card_id = ((card_point + 9) % 13) * 4 + card_suit
        group.add_card(card_id)
    elif command == 'remove' and len(input_str) == 3:
        card_suit = int(input_str[1])
        card_point = int(input_str[2])
        card_id = ((card_point + 9) % 13) * 4 + card_suit
        group.remove_card(card_id)
    elif command == 'exit':
        break

    print("当前牌组信息如下:")
    print("决定牌:", end="")
    show(group.deter_ID)
    print('Value:', group.value)
    group.showcard()



# updated 2024年10月22日12点58分