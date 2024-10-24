from message import Message, MessagePool
from Cardgroup import Cardgroup
from game_logic import *
import socket
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

class Room:
    def __init__(self):
        self.player_sockets:dict[int, socket.socket] = {}               # 玩家套接字
        self.usernames:dict[int,str] = {}                               # 玩家用户名
        self.cards = list(range(52))                                    # 牌
        self.carddict: dict[int, list[int]] = {}                        # 玩家手牌
        self.currentPlayer = -1                                         # 当前出牌玩家
        self.last_player = -1                                           # 上一个出牌玩家
        self.last_play = []                                             # 上一次出的牌

        self.group_black = []                                           # 黑队
        self.group_red = []                                             # 红队
        self.win_order = []                                             # 胜利顺序
        self.black_over = []                                            # 黑队出完牌的玩家
        self.red_over = []                                              # 红队出完牌的玩家
        self.score = [0, 0, 0, 0]                                       # 积分
        self.i = -1                                                     # 给玩家分配的id

        self.over = False                                               # 游戏结束
        self.time_limit = 30                                            # 出牌时间限制
        self.timer = None                                               # 计时器
        self.message_pool = MessagePool()                               # 消息池
        self.lock = threading.Lock()                                    # 锁



    def work(self):
        print("房间已启动")
        threading.Thread(target=self.process_send_message).start()
        while True:
            if self.is_full():
                print("房间已满,开始发牌")
                self.deal()
                break


    def is_full(self):
        return len(self.player_sockets) == 4

    def add_player(self, clientSocket, username):
        # 添加玩家信息 这里可以学习一下锁的用法
        with self.lock:
            self.i += 1
            self.player_sockets[self.i] = clientSocket
            self.usernames[self.i] = username
        threading.Thread(target=self.handle, args=(self.i,)).start()

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
                msg = Message.deserialize(clientSocket.recv(1024))
                if not msg:
                    self.remove_player(player_id)
                    break
                if msg.type == 'play':
                    # 出牌功能
                    # 只有当前玩家才能出牌
                    if self.currentPlayer == player_id:
                        self.receive_play(player_id, msg.content)
                    # 不是当前玩家 忽略请求
                    else:
                        continue
                elif msg.type == 'pass':
                    pass
                elif msg.type == 'chat':
                    # 聊天功能
                    self.receive_chat(player_id, msg.content)
                elif msg.type == 'quit':
                    # 玩家退出 具体释放逻辑由remove_player完成
                    self.remove_player(player_id)
                    break

            except Exception as e:
                print(f'Failed to receive message from client, {e}')
                self.remove_player(player_id)
                break
        return
        
    # 移除玩家
    def remove_player(self, player_id:int):
        # 由于这个函数会在多个函数中调用 所以要判断是否已经移除
        pass

    
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
    #endregion

    # 发牌 并确定队伍以及先出牌的玩家
    def deal(self):
        random.shuffle(self.cards)
        for player_id in range(4):
            # 玩家手牌 顺便排序
            playercards = sorted(self.cards[player_id*13:(player_id+1)*13])
            if 0 in playercards:# 方片4
                self.currentPlayer = player_id
                self.last_player = player_id
            if 51 in playercards:# 黑桃3
                self.group_black.append(player_id)
            #这个elif可以防止黑桃3和黑桃A是同一个人的时候把同一个人加到黑队里面两次
            elif 49 in playercards:# 黑桃A
                self.group_black.append(player_id)
            else:
                self.group_red.append(player_id)# 其余
            self.carddict[player_id] = playercards#服务器需要同步玩家手牌
            self.send_client_message(player_id, Message('handcard', playercards))
    
    # 广播等待玩家

    # 给新玩家发送当前房间信息

    # 广播新玩家加入

    # 广播游戏开始

    # 广播当前出牌权以及上一次出的牌
    def broadcast_current(self):
        self.broadcast(Message('current', [self.currentPlayer, self.last_play]).serialize())

    # 广播聊天信息

    # 处理出牌信息
    def receive_play(self, player_id:int, cardg:Cardgroup):
        if not check_play(cardg):
            return 
        self.last_play = cardg
        self.carddict[player_id] = [i for i in self.carddict[player_id] if i not in cardg.cards]
        # 出完牌后检查是否游戏结束
        if len(self.carddict[player_id]) == 0:
            self.check_over(player_id)
        self.next_turn()

    # 处理聊天信息
    def receive_chat(self, player_id, chat):
        pass

    
    # 计时器
    def start_trun(self):
        self.timer = threading.Timer(self.time_limit, self.time_up)
        self.timer.start()

    def time_up(self):
        self.force_play(self.currentPlayer)
        self.next_turn()
    
    # 下一个玩家出牌
    # 当更新完上一次出牌以及新的手牌之后调用
    def next_turn(self):
        self.timer.cancel()
        self.currentPlayer = (self.currentPlayer + 1) % 4
        self.broadcast_current()
        self.start_trun()

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
                self.over = True
                return
            # 红赢
            elif(self.win_order[0] in self.group_red and self.win_order[1] in self.group_red):
                self.score[self.group_red[0]] += 2
                self.score[self.group_red[1]] += 2
                self.score[self.group_black[0]] -= 2
                self.score[self.group_black[1]] -= 2
                self.over = True
                return
            # 黑红混合 这时候win_order的长度至少为3
            # 黑红黑 win_order[1]不用判断 因为前面已经判断过了
            elif(self.win_order[0] in self.group_black and self.win_order[2] in self.group_black):
                self.score[self.group_black[0]] += 1
                self.score[self.group_black[1]] += 1
                self.score[self.group_red[0]] -= 1
                self.score[self.group_red[1]] -= 1
                self.over = True
                return
            # 红黑红
            elif(self.win_order[0] in self.group_red and self.win_order[2] in self.group_red):
                self.score[self.group_red[0]] += 1
                self.score[self.group_red[1]] += 1
                self.score[self.group_black[0]] -= 1
                self.score[self.group_black[1]] -= 1
                self.over = True
                return
            # 平局 积分不变
            else:
                self.over = True
                return
        # 2.黑桃三和黑桃A是同一个人(独狼)的情况
        elif len(self.group_black) == 1 and len(self.group_red) == 3:
            # 黑是第一个赢的 +3 -1 -1 -1
            if(self.win_order[0] in self.group_black):
                self.score[self.group_black[0]] += 3
                for i in self.group_red:
                    self.score[i] -= 1
                self.over = True
                return
            # 黑是第二个赢的 0 +2 -1 -1
            elif(self.win_order[1] in self.group_black):
                self.score[self.group_black[0]] += 2
                red_win = self.win_order[0]
                for i in self.group_red:
                    if i != red_win:
                        self.score[i] -= 1
                self.over = True
                return
            # 黑是第三个赢的 +1 +1 -2 0
            elif(self.win_order[2] in self.group_black):
                self.score[self.group_black[0]] -= 2
                self.score[self.win_order[0]] += 1
                self.score[self.win_order[1]] += 1
                self.over = True
                return
            # 黑是最后一个赢的 +1 +1 +1 -3
            elif(self.win_order[3] in self.group_black):
                self.score[self.group_black[0]] -= 3
                for i in self.group_red:
                    self.score[i] += 1
                self.over = True
                return
            # 实际上不会出现这种情况
            else:
                self.over = True
                return
        # 实际上也不会出现这种情况
        else:
            self.over = True
            return

    # 输入玩家id 强制其出牌
    def force_play(self, player_id:int):
        # 强制出牌有两种情况
        # 1.如果上一次出牌的是自己 那么可以随便出牌 默认出最小的一张牌
        if self.currentPlayer == player_id:
            self.carddict[player_id].sort()
            self.last_play = [self.carddict[player_id][0]]
            self.carddict[player_id] = self.carddict[player_id][1:]
            self.next_turn()
        # 2.如果上一次出牌的不是自己 那么默认不出牌
        else:
            # 这里不能写self.last_play = []
            # 因为这样会导致下一个玩家出牌的时候判断出牌是否符合逻辑的时候出错
            # 只需要开始下一个玩家的计时器即可
            self.next_turn()

