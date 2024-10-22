from Cardgroup import *

def check_play(lastcards: Cardgroup, currcard: Cardgroup) -> bool:
    if currcard.type == -1:
        return False
    if lastcards.type <= 3:#这时候只能对应接牌
        if lastcards.type != currcard.type:
            return False
        else:#类型相同 直接比较
            return currcard.value > lastcards.value
    if lastcards.type == currcard.type:#类型相同 直接比较
        return currcard.value > lastcards.value
    else:
        return currcard.type > lastcards.type

