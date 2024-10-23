from src.message import *
from src.room import *
import socket
import threading




class Server:

    # 初始化服务器套接字
    def __init__(self):
        self.room:dict[int, Room] = {}                                                          # key为房间号 value为Room对象                                  
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #服务器套接字
        self.serverSocket.bind(('0.0.0.0', 12345))

    # 开始监听客户端连接
    def start(self):
        self.serverSocket.listen(50)
        while True:
            # 连接并启动线程
            clientSocket, addr = self.serverSocket.accept()
            threading.Thread(target=self.handle, args=(clientSocket,)).start()

    # 这个方法用于处理玩家刚连接时到进入房间的过程
    # 开新线程是为了不阻塞主线程
    def handle(self, clientSocket: socket.socket) -> None:
        while True:
            # 连接成功后输入房间号和用户名
            message = Message.deserialize(clientSocket.recv(1024))
            room_id = message.content[0]
            username = message.content[1]
            # 如果房间号不存在则创建房间
            if room_id not in self.room:
                self.room[room_id] = Room()
                threading.Thread(target=self.room[room_id].work).start()
                self.room[room_id].add_player(clientSocket, username)
                break
            # 如果房间号存在 则先判断房间是否已满 再判断名字是否重复
            else:
                if self.room[room_id].is_full():
                    clientSocket.send(Message('reroom_id', -1).serialize())
                    continue
                elif username in self.room[room_id].usernames.values():
                    clientSocket.send(Message('rename', -1).serialize())
                    continue
                else:
                    self.room[room_id].add_player(clientSocket, username)
                    break
        # 剩下的逻辑交给room处理 server不用管了
        return

