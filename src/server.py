from src.message import Message
from src.game_logic import *
import socket
import threading
import time
import random

'''
游戏流程以及服务器需要实现的功能
1.四个玩家连接后 输入用户名
2.进入房间 等待其他玩家进入
3.四个进入并全都准备后 服务器开始发牌
4.服务器发牌 确定每个玩家的id 积分 队伍 有方块4的玩家获得出牌权
5.游戏开始后 服务器不断广播当前出牌权以及上一次出的牌
6.服务器不断接收客户端的消息 判断出牌是否符合逻辑 并广播给其他客户端
7.当某一队的玩家出完牌后 游戏结束 计算积分(积分功能待定 先实现游戏基本逻辑)
8.游戏结束后可以选择重新开始游戏
'''


class Server:

    # 初始化服务器套接字
    def __init__(self):
        #以下三个字典的键都是玩家id
        self.clients = {}                           # 玩家套接字列表
        self.usernames = {}                         # 玩家用户名
        self.carddict = {}                          # 玩家手牌

        #时间控制变量
        self.timer = None                           # 计时器
        self.time_limit = 30                        # 时间限制

        self.currentPlayer = -1                     # 当前玩家
        self.last_play = []                         #上次出的牌
        self.group_black = []                       # 黑桃3和黑桃A
        self.group_red = []                         # 其余
        self.black_over = []                        # 黑桃出完牌的玩家
        self.red_over = []                          # 其余出完牌的玩家
        self.score = [0,0,0,0]                      # 积分

        # 注意A3没有大小王
        # 0是方片4 1是梅花4 51是黑桃3 依次类推
        self.cards = [i for i in range(52)]
        
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #服务器套接字
        self.serverSocket.bind(('0.0.0.0', 12345))

    # 开始监听客户端连接
    # 需要四个人才能开始游戏
    def start(self):
        self.serverSocket.listen(50)
        while True:
            i = 0 # 玩家id
            # 连接并启动线程
            clientSocket, addr = self.serverSocket.accept()
            self.clients.append(clientSocket)
            threading.Thread(target=self.handle, args=(clientSocket, i)).start()
            i += 1

            print('New connection:', addr)
            if(len(self.clients) == 4):
                self.broadcast('Game starts!'.encode('utf-8'))
                break
            else:
                self.broadcast('Waiting for other players to join...'.encode('utf-8'))
        self.game_start()


    # 接受客户端消息
    def handle(self, clientSocket, player_id):
        # 发送玩家id
        clientSocket.send(Message('id', player_id).serialize())
        # 到时候客户端需要写一个输入用户名的界面
        username = clientSocket.recv(1024).decode('utf-8').strip()
        self.usernames[player_id] = username
        self.clients[player_id] = clientSocket
        # 广播新玩家加入 客户端到时候需要根据这个信息更新界面
        self.broadcast(Message('newplayer', [player_id, username]).serialize())

        # 接收消息
        while True:
            try:
                message = clientSocket.recv(1024)
                if not message:
                    break
                msg = Message.deserialize(message)
                if msg.type == 'play':
                    # 出牌功能
                    self.receive_play(player_id, msg.content)
                elif msg.type == 'chat':
                    # 聊天功能
                    self.receive_chat(player_id, msg.content)

            except Exception as e:
                print(f'Failed to receive message from client, {e}')
                break
        self.clients.remove(clientSocket)
        clientSocket.close()
        print('Connection closed')
        


    # 广播消息
    def broadcast(self, message):
        for client in self.clients:
            try:
                client.send(message)
            except Exception as e:
                print(f'Failed to send message to client, {e}')
                self.clients.remove(client)
                client.close()
    
    # 发牌 并确定队伍以及先出牌的玩家
    def deal(self):
        random.shuffle(self.cards)
        for player_id in range(4):
            # 玩家手牌 顺便排序
            playercards = sorted(self.cards[i*13:(i+1)*13])
            if 0 in playercards:# 方片4
                self.currentPlayer = player_id
            if 51 in playercards:# 黑桃3
                self.group_black.append(player_id)
            elif 49 in playercards:# 黑桃A
                self.group_black.append(player_id)
            else:
                self.group_red.append(player_id)# 其余
            self.carddict[player_id] = playercards#服务器需要同步玩家手牌
            self.clients[player_id].send(Message('handcard', playercards).serialize())
    
    # 广播当前出牌权以及上一次出的牌
    def broadcast_current(self):
        self.broadcast(Message('current', [self.currentPlayer, self.last_play]).serialize())

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
    
    def next_turn(self):
        self.timer.cancel()
        self.currentPlayer = (self.currentPlayer + 1) % 4
        self.broadcast_current()
        self.start_trun()

    def check_over(self, player_id:int):
        pass
    


    #游戏主循环
    def game_start(self):
        self.deal()
        self.broadcast_current()

        while True:
            pass