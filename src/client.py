from Cardgroup import *
from src.message import Message
import socket

class Client:

    # 初始化客户端
    def __init__(self):
        # 网络部分 初始化客户端套接字
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.player_id = -1
        self.handcard = Cardgroup()     # 手牌
        self.pickcard = Cardgroup()     # 选中的牌
        self.ableto_play = False        # 是否可以出牌

    # 连接服务器
    def connect(self):
        serverIP = "8.217.57.241"
        serverPort = 12345
        self.clientSocket.connect((serverIP, serverPort))
    
    # 发送数据给服务器
    def send(self, message):
        self.clientSocket.send(message)

    # 接收服务器数据
    def receive(self):
        message = self.clientSocket.recv(1024)
        msg = Message.deserialize(message)
        return msg
    
    def rev_handcard(self, message):
        for i in message.content:
            self.handcard.add_card(Card(i))
        self.handcard.sort()