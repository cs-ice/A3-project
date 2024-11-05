from Cardgroup import *

def check_play(last: list[int], curr: list[int]) -> bool:
    currcard = create_cardgroup(curr)
    # 这样意味着是第一次出牌 需要判断是否包含方块4
    if last == [-1]:
        return 0 in currcard.cards and currcard.type != -1
    
    # 这个在后面创建 毕竟怕出现-1 防止出现错误
    lastcard = create_cardgroup(last)
    if currcard.type == -1:
        return False
    # 这样意味着被接封了 可以随便出
    if last == []:
        return True
    if lastcard.type <= 3:#这时候只能对应接牌
        if lastcard.type != currcard.type:
            return False
        else:#类型相同 直接比较
            return currcard.value > lastcard.value
    if lastcard.type == currcard.type:#类型相同 直接比较
        return currcard.value > lastcard.value
    else:
        return currcard.type > lastcard.type

