from src.message import Message
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
        self.cards = [i for i in range(52)]
        
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#服务器套接字
        self.serverSocket.bind(('0.0.0.0', 12345))

    # 开始监听客户端连接
    # 需要四个人才能开始游戏
    def start(self):
        self.serverSocket.listen(50)
        while True:
            # 连接并启动线程
            clientSocket, addr = self.serverSocket.accept()
            self.clients.append(clientSocket)
            threading.Thread(target=self.handle, args=(clientSocket,)).start()

            print('New connection:', addr)
            if(len(self.clients) == 4):
                self.broadcast('Game starts!'.encode('utf-8'))
                break
            else:
                self.broadcast('Waiting for other players to join...'.encode('utf-8'))
    

    # 接受客户端消息
    def handle(self, clientSocket):
        while True:
            try:
                message = clientSocket.recv(1024)
                if not message:
                    break
                msg = Message.deserialize(message)
                
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
    # 发牌
    def deal(self):
        random.shuffle(self.cards)
        for i in range(4):
            self.clients[i].send(Message('deal', self.cards[i*13:(i+1)*13]).serialize())

    #endrigion