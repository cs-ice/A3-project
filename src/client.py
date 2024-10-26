from Cardgroup import *
from message import *
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

        self.myorder = -1               # 我的出牌顺序
        self.order = [0, 1, 2, 3]       # 玩家出牌顺序
        self.curr_order = -1            # 当前出牌的玩家顺序
        self.last_order = -1            # 上一个出牌的玩家顺序
        self.need_to_react = []         # 需要应对的牌
        self.order_to_act_dict = {}     # 所有玩家的上次出牌记录
        self.handcard = []              # 手牌
        self.ableto_play = False        # 是否可以出牌

        self.receive_lock = threading.Lock()

    # 这个while循环可能主要用于测试 实际中 建议用户输入信息后 点击按钮 触发sed_room_and_name
    # 这样的实现方式更符合实际
    def connect_to_room(self):
        while True:
            room_id = int(input("请输入房间号: "))
            username = input("请输入用户名: ")
            try:
                self.sed_room_and_name(room_id, username)
                break
            except Exception as e:
                print(e)
        self.test()
    
    # 接收服务器数据
    def receive(self, start_message: Message):
        msg = start_message#防止丢失进入房间后的第一条消息
        while True:
            if msg is None:
                continue
            if msg.type == "id":
                self.rev_id(msg)
            elif msg.type == "room_info":
                self.rev_room_info(msg)
            elif msg.type == "new_player":
                self.rev_new_player(msg)
            elif msg.type == "handcard":
                self.rev_handcard(msg)
            elif msg.type == "quit":
                self.rev_quit(msg)
            elif msg.type == "ready":
                self.rev_ready(msg)
            elif msg.type == "unready":
                self.rev_unready(msg)
            elif msg.type == "chat":
                self.rev_chat(msg)
            elif msg.type == "order":
                self.rev_order(msg)
            elif msg.type == "action":
                self.rev_action(msg)
            else:
                print("未知消息类型")
            msg = socket_recv(self.clientSocket)
    
    #region 发送消息

    # 发送数据给服务器
    def sendmsg(self, message: Message):
        self.clientSocket.send(message.serialize())
   
    # 尝试进入房间时 才和服务器连接
    def sed_room_and_name(self, room_id: int, username: str) ->bool:
        #serverIP = "8.217.57.241"       # 服务器ip地址
        serverIP = "127.0.0.1"           # 测试用本地ip
        serverPort = 12345
        self.clientSocket.connect((serverIP, serverPort))
        
        self.sendmsg(Message("roomAndName", [room_id, username]))
        msg = socket_recv(self.clientSocket)
        # 这些虽然算不上异常 但是可以用异常处理的方式来处理
        if msg is None:
            raise Exception("未接收到服务器信息")
        elif msg.type == "rename":
            raise Exception("用户名重复")
        elif msg.type == "reroom_id":
            raise Exception("房间已满")
        else:
            print("成功进入房间")
            threading.Thread(target=self.receive, args=(msg,)).start()
            return True

    def sed_ready(self):
        self.sendmsg(Message("ready", True))
    
    def sed_unready(self):
        self.sendmsg(Message("unready", False))
    
    def sed_chat(self, content: str):
        self.sendmsg(Message("chat", content))

    #endregion

    #region 接收消息

    # 处理服务器发来的新玩家信息
    def rev_id(self, message: Message):
        # 这里的message.content是一个int
        # 你的id
        self.player_id = message.content
        print("你的id是: ", self.player_id)

    def rev_room_info(self, message: Message):
        # 这里的message.content是一个dict
        # key是玩家id value是玩家名字
        print("当前房间内的玩家有: ", message.content)

    def rev_new_player(self, message: Message):
        # 这里的message.content是一个list
        # 0是id(int) 1是名字(str)
        player_id = message.content[0]
        player_name = message.content[1]
        print("新玩家加入, 他的id是:", player_id, "他的名字是:", player_name)
        pass
    
    def rev_handcard(self, message: Message):
        # 这里的message.content是一个list
        # 里面是降序排列的手牌
        for i in message.content:
            self.handcard.add_card(i)
        print("你的手牌是: ", self.handcard.cards)

    def rev_quit(self, message: Message):
        # 这里的message.content是一个int
        # 退出的玩家id
        print("玩家", message.content, "退出了房间")
        pass

    def rev_ready(self, message: Message):
        # 这里的message.content是一个int
        # 准备的玩家id
        print("玩家", message.content, "准备了")
    
    def rev_unready(self, message: Message):
        # 这里的message.content是一个int
        # 取消准备的玩家id
        print("玩家", message.content, "取消准备")

    def rev_chat(self, message: Message):
        # 这里的message.content是一个list
        # 0是id(int) 1是聊天内容(str)
        player_id = message.content[0]
        contentstr = message.content[1]
        print("玩家", player_id, "说: ", contentstr)

    def rev_order(self, message: Message):
        # 这里的message.content是一个list
        # 里面是玩家id的出牌顺序
        self.order = message.content
        for i in range(len(self.order)):
            if self.order[i] == self.player_id:
                self.myorder = i
                break

    def rev_action(self, message: Message):
        # 这里的message.content是一个list
        # 0是一个int 当前行动的玩家顺序(不是id)
        # 1是一个list 里面是上一个行动的玩家的行动 为[]代表不出
        # 2是一个list 里面是当前需要应对的玩家的牌 为[]代表不需要应对 即这是第一次出牌 需要出含有方块4的牌
        # 3是一个int 代表上一个出牌的玩家的顺序
        if message.content[2] != []:
            # 先进行这个操作 不然待会curr_order会更新
            self.order_to_act_dict[self.curr_order] = message.content[1]
        self.curr_order = message.content[0]
        self.need_to_react = message.content[2]
        self.last_order = message.content[3]
        if self.curr_order == self.myorder:
            self.ableto_play = True
        else:
            self.ableto_play = False

    #endregion

    def quit(self):
        self.sendmsg(Message("quit", True))
        self.clientSocket.close()
        pass

    # 测试代码
    def test(self):
        while True:
            command = input("请输入指令: ")
            if command == "ready":
                self.sed_ready()
            elif command == "unready":
                self.sed_unready()
            elif command == "quit":
                self.quit()
                break
            else:
                print("未知指令")




if __name__ == '__main__':
    client = Client()
    client.connect_to_room()
    