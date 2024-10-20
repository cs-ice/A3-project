import socket
import threading
import time
import random



class Server:

    # 初始化服务器套接字
    def __init__(self):
        self.clients = []# 玩家列表
        self.currentPlayer = 0# 当前玩家

        # 注意A3没有大小王
        self.cards = [0,  1,  2,  3,  4,  5,  6,  7,  8,  9,  10, 11, 12,#方块
                      13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,#梅花
                      26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38,#红桃
                      39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51,]#黑桃
        
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#服务器套接字
        self.serverSocket.bind(('0.0.0.0', 12345))

    # 开始监听客户端连接
    # 需要四个人才能开始游戏
    def start(self):
        self.serverSocket.listen(50)
        while True:
            clientSocket, addr = self.serverSocket.accept()
            self.clients.append(clientSocket)
            print('New connection:', addr)
            if(len(self.clients) == 4):
                self.broadcast('Game starts!')
                break
            else:
                self.broadcast('Waiting for other players to join...')
    
#region 游戏逻辑
    # 发牌
    def deal(self):
        random.shuffle(self.cards)
        self.sendbytype('deal')
        
        

    # 出牌
    def play(self):
        pass

    # 结算
    def settle(self):
        pass

    # 聊天
    def chat(self):
        pass

    # 重置游戏
    def reset(self):
        pass


#endregion


#region 接收信息

    # 接收玩家的出牌信息

    # 接收玩家的聊天信息

    # 接收玩家的准备信息

#endregion

#region 发送信息
    # 广播信息的总函数
    def sendbytype(self, messagetype, message = ''):
        if(messagetype == 'chat'):
            pass
        elif(messagetype == 'play'):
            pass
        elif(messagetype == 'deal'):
            self.senddeal()
            pass
        elif(messagetype == 'settle'):
            pass

    # 广播游戏开始信息
    
    # 广播发牌信息
    def senddeal(self):
        for i in range(4):
            message = self.cards[i*13:(i+1)*13].encode()
            self.clients[i].send(message)

    # 广播出牌信息

    # 广播聊天信息

    # 广播游戏结束信息

#endregion