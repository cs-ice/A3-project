from Cardgroup import *

def check_play(last: list[int], curr: list[int]) -> bool:
    # 这样意味着是第一次出牌 需要判断是否包含方块4
    if last == []:
        return 0 in curr
    lastcard = create_cardgroup(last)
    currcard = create_cardgroup(curr)
    if currcard.type == -1:
        return False
    if lastcard.type <= 3:#这时候只能对应接牌
        if lastcard.type != currcard.type:
            return False
        else:#类型相同 直接比较
            return currcard.value > lastcard.value
    if lastcard.type == currcard.type:#类型相同 直接比较
        return currcard.value > lastcard.value
    else:
        return currcard.type > lastcard.type

