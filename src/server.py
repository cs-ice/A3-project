from src.message import Message
import socket
import threading
import time
import random

'''
游戏流程以及服务器需要实现的功能
1.四个玩家连接后开始游戏
2.服务器发牌 确定每个玩家的id  积分 有方块4的玩家先出牌
3.这个优先出牌的规则需要在客户端出牌的时候也写对应的逻辑
4.服务器还需要确定两队的逻辑 黑桃3和黑桃A是一队 其余是一队
5.所以在发牌时 需要判断发出去的牌是否包含黑桃3和黑桃A以及方块4 来确定游戏的内部逻辑
6.服务器不断接收客户端的消息 判断出牌是否符合逻辑 并广播给其他客户端
7.当某一队的玩家出完牌后 游戏结束 计算积分(积分功能待定 先实现游戏基本逻辑)
8.游戏结束后可以选择重新开始游戏
'''


class Server:

    # 初始化服务器套接字
    def __init__(self):
        self.clients = []# 玩家套接字列表
        self.currentPlayer = -1# 当前玩家
        self.carddict = {}# 玩家手牌
        self.last_play = []#上次出的牌
        self.group_black = []# 黑桃3和黑桃A
        self.group_red = []# 其余
        self.score = [0,0,0,0]# 积分

        # 注意A3没有大小王
        # 0是方片4 1是梅花4 51是黑桃3 依次类推
        self.cards = [i for i in range(52)]
        
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#服务器套接字
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
        while True:
            try:
                message = clientSocket.recv(1024)
                if not message:
                    break
                msg = Message.deserialize(message)
                if msg.type == 'play':
                    self.receive_play(player_id, msg.content)


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
    
    #region 游戏逻辑
    # 发牌 并确定队伍以及先出牌的玩家
    def deal(self):
        random.shuffle(self.cards)
        for i in range(4):
            # 玩家手牌 顺便排序
            playercards = sorted(self.cards[i*13:(i+1)*13])
            if 0 in playercards:# 方片4
                self.currentPlayer = i
            if 51 in playercards:# 黑桃3
                self.group_black.append(i)
            elif 49 in playercards:# 黑桃A
                self.group_black.append(i)
            else:
                self.group_red.append(i)# 其余
            self.carddict[i] = playercards#服务器需要同步玩家手牌
            self.clients[i].send(Message('handcard', playercards).serialize())
    
    # 广播当前出牌权以及上一次出的牌
    def broadcast_current(self):
        self.broadcast(Message('current', [self.currentPlayer, self.last_play]).serialize())

    # 接收玩家出的牌 并判断是否符合规则 
    # 符合规则则在服务器中更新手牌
    def receive_play(self, player_id, play):
        if not self.check_play(play):
            return 
        self.last_play = play
        self.carddict[player_id] = [i for i in self.carddict[player_id] if i not in play]
        self.currentPlayer = (self.currentPlayer + 1) % 4
        self.broadcast_current()


    #endrigion

    #游戏主循环
    def game_start(self):
        self.deal()
        self.broadcast_current()
        while True:
            pass