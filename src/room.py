from message import *
from Cardgroup import Cardgroup
from game_logic import *
import threading
import random

'''
游戏流程
1.四个玩家连接后 输入用户名
2.进入房间 等待其他玩家进入
3.四个进入并全都准备后 服务器开始发牌
4.服务器发牌 确定每个玩家的id 积分 队伍 有方块4的玩家获得出牌权
5.游戏开始后 服务器不断广播当前出牌权以及上一次出的牌
6.服务器不断接收客户端的消息 判断出牌是否符合逻辑 并广播给其他客户端
7.当某一队的玩家出完牌后 游戏结束 计算积分(积分功能待定 先实现游戏基本逻辑)
8.游戏结束后可以选择重新开始游戏
'''

'''
下面大多数是从原来的server.py中拷贝过来的
现在需要对server.py进行重构
由room负责游戏房间的逻辑
server.py负责游戏房间的创建以及维护
'''

'''
2024.10.25
下一步实现的功能
玩家准备
玩家退出
'''


class Room:
    def __init__(self):
        self.player_sockets:dict[int, socket.socket] = {}               # 玩家套接字
        self.usernames:dict[int,str] = {}                               # 玩家用户名
        self.cards = list(range(52))                                    # 牌
        self.carddict: dict[int, list[int]] = {}                        # 玩家手牌
        self.current_order = -1                                         # 当前出牌顺序
        self.last_order = -1                                            # 出需要应对的牌的玩家的顺序
        self.last_play = []                                             # 目前需要应对的牌
        self.last_act = []                                              # 上一次行动
        self.order = [0, 1, 2 ,3]                                       # 出牌顺序

        self.group_black = []                                           # 黑队
        self.group_red = []                                             # 红队
        self.win_order = []                                             # 胜利顺序
        self.black_over = []                                            # 黑队出完牌的玩家
        self.red_over = []                                              # 红队出完牌的玩家
        self.score = [0, 0, 0, 0]                                       # 积分
        self.win = [False, False, False, False]                         # 胜利情况
        self.idstack = [3, 2, 1, 0]                                     # 给玩家分配id的栈

        self.is_full = False                                            # 房间是否满员
        self.is_ready = [False, False, False, False]                    # 玩家是否准备
        self.over = False                                               # 游戏结束
        self.time_limit = 30                                            # 出牌时间限制
        self.timer = None                                               # 计时器
        self.message_pool = MessagePool()                               # 消息池
        self.lock = threading.Lock()                                    # 锁

    def work(self):
        print("房间已启动")
        threading.Thread(target=self.process_send_message).start()
        while True:
            if self.all_ready():
                self.sed_order()
                print("所有玩家准备完毕 发送出牌顺序以及初始出牌权")
                self.sed_begin_cards()
                self.sed_action(self.current_order, [],[-1], self.current_order)
                self.start_trun()
                for i in range(4):
                    self.is_ready[i] = False
                break

    def is_empty(self):
        return len(self.idstack) == 4

    def all_ready(self):
        for i in self.is_ready:
            if not i:
                return False
        return True

    def add_player(self, clientSocket, username):
        # 添加玩家信息 这里可以学习一下锁的用法
        with self.lock:
            id = self.idstack.pop()
            if len(self.idstack) == 0:
                self.is_full = True
            self.player_sockets[id] = clientSocket
            self.usernames[id] = username
        threading.Thread(target=self.handle, args=(id,)).start()

    #region 服务器接受客户端消息

    # 接受客户端消息
    def handle(self, player_id:int):
        clientSocket = self.player_sockets[player_id]
        # 发送玩家id
        self.send_client_message(player_id, Message('id', player_id))

        # 向新玩家发送当前房间信息
        current_players = self.usernames
        self.send_client_message(player_id, Message('room_info', current_players))

        # 广播新玩家加入 客户端到时候需要根据这个信息更新界面
        self.broadcast_message(Message('new_player', [player_id, self.usernames[player_id]]))

        # 接收消息
        while True:
            try:
                msg = socket_recv(clientSocket)
                if not msg:
                    continue
                if msg.type == 'play':
                    self.rev_play(player_id, msg.content)
                elif msg.type == 'ready':
                    self.rev_ready(player_id)
                elif msg.type == 'unready':
                    self.rev_unready(player_id)
                elif msg.type == 'pass':
                    self.rev_pass(player_id)
                elif msg.type == 'chat':
                    # 聊天功能
                    self.rev_chat(player_id, msg.content)
                elif msg.type == 'quit':
                    # 玩家退出 具体释放逻辑由remove_player完成
                    self.remove_player(player_id)
                    break

            except Exception as e:
                print(f'Failed to receive message from client, {e}')
                self.remove_player(player_id)
                break
        return
        
    def rev_ready(self, player_id:int):
        self.is_ready[player_id] = True
        self.broadcast_message(Message('ready', player_id))

    def rev_unready(self, player_id:int):
        self.is_ready[player_id] = False
        self.broadcast_message(Message('unready', player_id))

    def rev_pass(self, player_id:int):
        # 只有当前玩家才能pass
        if self.current_order == self.id_to_order(player_id):
            # pass相当于不出牌
            self.last_act = []
            self.next_turn()
        else:
            return

    def rev_play(self, player_id:int, cardg: list[int]):
        # 只有当前玩家才能出牌
        if self.current_order != self.id_to_order(player_id):
            return
        # 出牌逻辑
        if not check_play(self.last_play, cardg):
            return 
        self.last_play = cardg
        self.last_act = cardg
        self.last_order = self.current_order
        self.carddict[player_id] = [i for i in self.carddict[player_id] if i not in cardg]
        # 出完牌后检查是否游戏结束
        if len(self.carddict[player_id]) == 0:
            if self.check_over(player_id):
                # 游戏结束 调用对应的逻辑 无需开启下一个turn
                # 这时候game_over函数已经计算完积分
                # 这时候需要广播两个信息
                # 1.最后一次出牌的信息
                # 2.积分信息
                self.sed_action(self.current_order, self.last_act, self.last_play, self.last_order)
                self.sed_score()
                # 更新完积分后再把房间的状态重置
                self.over = True
                return
        self.next_turn()

    def rev_chat(self, player_id, chat):
        self.broadcast_message(Message('chat', [player_id, chat]))

    #endregion

    # 移除玩家
    def remove_player(self, player_id:int) -> None:
        # 由于这个函数会在多个函数中调用 所以要判断是否已经移除
        if player_id in self.idstack:
            return
        with self.lock:
            self.idstack.append(player_id)
            self.is_ready[player_id] = False
            self.is_full = False
            self.player_sockets.pop(player_id)
            self.usernames.pop(player_id)
        self.broadcast_message(Message('quit', player_id))
        return
        
    
    #region 消息处理 其他函数想要发送消息都要调用brodcast_message或者send_client_message
    def broadcast_message(self, message:Message):
        self.message_pool.add_broadcast_message(message)

    def send_client_message(self, player_id:int, message:Message):
        self.message_pool.add_client_message(player_id, message)

    # 发送消息全部由这个函数处理
    def process_send_message(self):
        while True:
            with self.lock:
                for pid, client in self.player_sockets.items():
                    if self.message_pool.has_client_message(pid):
                        message = self.message_pool.get_next_client_message(pid)
                        if message:
                            client.send(message.serialize())
            if self.message_pool.has_broadcast_message():
                message = self.message_pool.get_next_broadcast_message()
                if message:
                    with self.lock:
                        for client in self.player_sockets.values():
                            client.send(message.serialize())

    # 发牌 并确定队伍以及先出牌的玩家
    def sed_begin_cards(self):
        random.shuffle(self.cards)
        for player_id in range(4):
            # 玩家手牌 顺便排序
            playercards = sorted(self.cards[player_id*13:(player_id+1)*13], reverse=True)
            if 0 in playercards:# 方片4
                for i in range(4):
                    if self.order[i] == player_id:
                        self.current_order = i
                        self.last_order = i
                        break
            if 51 in playercards:# 黑桃3
                self.group_black.append(player_id)
            #这个elif可以防止黑桃3和黑桃A是同一个人的时候把同一个人加到黑队里面两次
            elif 49 in playercards:# 黑桃A
                self.group_black.append(player_id)
            else:
                self.group_red.append(player_id)# 其余
            self.carddict[player_id] = playercards#服务器需要同步玩家手牌
            self.sed_handcard(player_id)

    def sed_handcard(self, player_id:int):
        self.carddict[player_id].sort(reverse=True)
        self.send_client_message(player_id, Message('handcard', self.carddict[player_id]))
    
    def sed_action(self, curr_act_order:int, last_act: list[int], need_react_cards: list[int], last_act_order:int):
        # curr_act_player是当前出牌玩家
        # last_act是上家出的牌如果是[] 则表示上家pass 
        # need_react_cards当前需要应对的牌 如果是[-1] 则表示这是第一次出牌 需要判断是否有方块4
        # last_act_player是上家出牌玩家 如果是玩家自己 则此时玩家可以随便出牌
        self.broadcast_message(Message('action', [curr_act_order, last_act, need_react_cards, last_act_order]))

    def sed_order(self):
        random.shuffle(self.order)
        self.broadcast_message(Message('order', self.order))

    def sed_score(self):
        # 注意score是一个list 且下标和player_id是一一对应的 不是和order对应
        self.broadcast_message(Message('score', self.score))

    #endregion

    # 一些辅助函数
    def id_to_order(self, player_id:int) -> int:
        for i in range(4):
            if self.order[i] == player_id:
                return i
        return -1
    
    def order_to_id(self, order:int) -> int:
        return self.order[order]
    

    # 计时器
    def start_trun(self):
        self.timer = threading.Timer(self.time_limit, self.time_up)
        self.timer.start()

    def time_up(self):
        self.force_play(self.current_order)
        self.next_turn()
    
    # 下一个玩家出牌
    # 当更新完上一次出牌以及新的手牌之后调用
    def next_turn(self):
        self.timer.cancel()
        # 单独给current_order的玩家发送手牌信息
        self.sed_handcard(self.order_to_id(self.current_order))
        self.order_change()
        self.sed_action(self.current_order, self.last_act, self.last_play, self.last_order)
        self.start_trun()

    # 更新出牌权
    def order_change(self):
        temp = self.current_order = (self.current_order + 1) % 4
        # 如果下一个玩家没有手牌 则跳过
        # 游戏的规则决定了这个while循环一定会结束 因为不可能至少有一个玩家有手牌
        while self.carddict[self.order_to_id(temp)] == []:
            if temp == self.last_order:
                # 如果上出完牌的玩家的牌一直没人要 那么下一个玩家就可以随便出牌
                self.last_play = []
            temp = (temp + 1) % 4
        self.current_order = temp

    # 输入出完牌的玩家id 判断游戏是否结束
    def check_over(self, player_id:int) -> bool:
        # 胜利顺序用来计算积分
        self.win_order.append(player_id)
        if player_id in self.group_black:
            self.black_over.append(player_id)
        else:
            self.red_over.append(player_id)
        if len(self.black_over) == len(self.group_black) or len(self.red_over) == len(self.group_red):
            # 当进入这个if语句 一定是游戏结束的情况
            self.game_over()
            return True
        return False
    
    # 根据游戏结束时的情况判断胜利方 计算积分
    def game_over(self):
        # 游戏结束的各种情况
        # 1.正常的2对2
        if len(self.group_black) == 2 and len(self.group_red) == 2:
            #1,2对3,4的局面
            # 黑赢
            if(self.win_order[0] in self.group_black and self.win_order[1] in self.group_black):
                self.score[self.group_black[0]] += 2
                self.score[self.group_black[1]] += 2
                self.score[self.group_red[0]] -= 2
                self.score[self.group_red[1]] -= 2
                return
            # 红赢
            elif(self.win_order[0] in self.group_red and self.win_order[1] in self.group_red):
                self.score[self.group_red[0]] += 2
                self.score[self.group_red[1]] += 2
                self.score[self.group_black[0]] -= 2
                self.score[self.group_black[1]] -= 2
                return
            # 黑红混合 这时候win_order的长度至少为3
            # 黑红黑 win_order[1]不用判断 因为前面已经判断过了
            elif(self.win_order[0] in self.group_black and self.win_order[2] in self.group_black):
                self.score[self.group_black[0]] += 1
                self.score[self.group_black[1]] += 1
                self.score[self.group_red[0]] -= 1
                self.score[self.group_red[1]] -= 1
                return
            # 红黑红
            elif(self.win_order[0] in self.group_red and self.win_order[2] in self.group_red):
                self.score[self.group_red[0]] += 1
                self.score[self.group_red[1]] += 1
                self.score[self.group_black[0]] -= 1
                self.score[self.group_black[1]] -= 1
                return
            # 平局 积分不变
            else:
                return
        # 2.黑桃三和黑桃A是同一个人(独狼)的情况
        elif len(self.group_black) == 1 and len(self.group_red) == 3:
            # 黑是第一个赢的 +3 -1 -1 -1
            if(self.win_order[0] in self.group_black):
                self.score[self.group_black[0]] += 3
                for i in self.group_red:
                    self.score[i] -= 1
                return
            # 黑是第二个赢的 0 +2 -1 -1
            elif(self.win_order[1] in self.group_black):
                self.score[self.group_black[0]] += 2
                red_win = self.win_order[0]
                for i in self.group_red:
                    if i != red_win:
                        self.score[i] -= 1
                return
            # 黑是第三个赢的 +1 +1 -2 0
            elif(self.win_order[2] in self.group_black):
                self.score[self.group_black[0]] -= 2
                self.score[self.win_order[0]] += 1
                self.score[self.win_order[1]] += 1
                return
            # 黑是最后一个赢的 +1 +1 +1 -3
            elif(self.win_order[3] in self.group_black):
                self.score[self.group_black[0]] -= 3
                for i in self.group_red:
                    self.score[i] += 1
                return
            # 实际上不会出现这种情况
            else:
                return
        # 实际上也不会出现这种情况
        else:
            return

    # 输入玩家id 强制其出牌
    def force_play(self, player_order:int):
        # 强制出牌有两种情况
        # 1.如果上一次出牌的是自己 那么可以随便出牌 默认出最小的一张牌
        if self.last_order == player_order:
            id = self.order_to_id(player_order)
            # 强制出最小的一张牌
            self.carddict[id].sort()
            # 更新信息 注意下面两个语句的顺序不能颠倒
            self.last_play = [self.carddict[id][0]]
            self.carddict[id] = self.carddict[id][1:]
            self.last_act = self.last_play
            self.last_order = player_order
                    # 出完牌后检查是否游戏结束
            if len(self.carddict[id]) == 0:
                if self.check_over(id):
                    # 游戏结束 调用对应的逻辑 无需开启下一个turn
                    # 这时候game_over函数已经计算完积分
                    # 这时候需要广播两个信息
                    # 1.最后一次出牌的信息
                    # 2.积分信息
                    self.sed_action(self.current_order, self.last_act, self.last_play, self.last_order)
                    self.sed_score()
                    # 更新完积分后再把房间的状态重置
                    self.over = True
                    return
        # 2.如果上一次出牌的不是自己 那么默认不出牌
        else:
            # 这里不能写self.last_play = []
            # 因为这样会导致下一个玩家出牌的时候判断出牌是否符合逻辑的时候出错
            # 只需要开始下一个玩家的计时器即可
            self.last_act = []

