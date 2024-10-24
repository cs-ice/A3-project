from Cardgroup import *
from message import Message
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
        self.receive_lock = threading.Lock()

    # 连接服务器
    def connect_to_room(self):
        #serverIP = "8.217.57.241"       # 服务器ip地址
        serverIP = "172.27.130.221"     # 测试用本地ip
        serverPort = 12345
        self.clientSocket.connect((serverIP, serverPort))
        
        # 输入房间号和用户名
        room_id = input("请输入房间号: ")
        username = input("请输入用户名: ")
        self.clientSocket.send(Message("roomAndName", [int(room_id), username]).serialize())
        msg = Message.deserialize(self.clientSocket.recv(1024))
        while msg is None or msg.type == "rename" or msg.type == "reroom_id":
            if msg is None:
                continue
            if msg.type == "rename":
                print("用户名重复, 请重新输入")
            else:
                print("房间已满或不存在, 请重新输入")
            room_id = input("请输入房间号: ")
            username = input("请输入用户名: ")
            self.clientSocket.send(Message("roomAndName", [int(room_id), username]).serialize())
            msg = Message.deserialize(self.clientSocket.recv(1024))
        print("成功进入房间")
        threading.Thread(target=self.receive, args=(msg,)).start()
    
    # 接收服务器数据
    def receive(self, start_message: Message):
        while True:
            message = self.clientSocket.recv(1024)
            msg = Message.deserialize(message)
            if msg is None:
                continue
            if msg.type == "id":
                self.player_id = msg.content
                print("你的id是: ", self.player_id)
            elif msg.type == "room_info":
                print("当前房间内的玩家有: ", msg.content)
            elif msg.type == "new_player":
                self.rev_new_player(msg)
            elif msg.type == "handcard":
                self.rev_handcard(msg)
            pass
    
    # 发送数据给服务器
    def sendmsg(self, message: Message):
        self.clientSocket.send(message.serialize())

    # 处理服务器发来的新玩家信息
    def rev_new_player(self, message: Message):
        print("新玩家加入, 他的id是:", message.content[0], "他的名字是:", message.content[1])
        pass
    
    def rev_handcard(self, message: Message):
        for i in message.content:
            self.handcard.add_card(i)
        print("你的手牌是: ", self.handcard.cards)

    # 测试代码
    def test(self):
        pass



if __name__ == '__main__':
    client = Client()
    client.connect_to_room()
    