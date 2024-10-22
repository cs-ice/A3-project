from Cardgroup import *
from src.message import Message
import socket
import threading

'''
游戏流程以及客户端需要实现的功能
1.服务器发来的基本信息 玩家id 手牌等
2.其余三位玩家的手牌数
3.接收最后一次出牌的玩家id以及出的牌(因为最后出牌的不一定是上家)
4.不断比较玩家当前选中的牌是否符合规则并大于上家 若符合则可以出牌
5.若最后一次出牌的玩家id为自己则依旧可以出牌
6.同时不断接收服务器发来的消息
7.游戏结束由服务器判断
'''

class Client:

    # 初始化客户端
    def __init__(self):
        # 网络部分 初始化客户端套接字
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.player_id = -1
        self.handcard = Cardgroup()     # 手牌
        self.pickcard = Cardgroup()     # 选中的牌
        self.ableto_play = False        # 是否可以出牌
        self.last_play = Cardgroup()    # 上一次出的牌

    # 连接服务器
    def connect(self):
        serverIP = "8.217.57.241"
        serverPort = 12345
        self.clientSocket.connect((serverIP, serverPort))
        threading.Thread(target=self.receive).start()
    
    # 发送数据给服务器
    def send(self, message):
        self.clientSocket.send(message)

    # 接收服务器数据
    def receive(self):
        while True:
            message = self.clientSocket.recv(1024)
            msg = Message.deserialize(message)
            if msg.type == 'handcard':
                self.rev_handcard(msg)
            pass

    
    def rev_handcard(self, message):
        for i in message.content:
            self.handcard.add_card(i)
