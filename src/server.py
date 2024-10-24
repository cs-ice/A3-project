from message import *
from room import *
import threading




class Server:

    # 初始化服务器套接字
    def __init__(self):
        self.room:dict[int, Room] = {}                                          # key为房间号 value为Room对象                                  
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #服务器套接字
        self.serverSocket.bind(('0.0.0.0', 12345))
        self.lock = threading.Lock()                                            # 锁保证线程安全

    # 开始监听客户端连接
    def start(self):
        self.serverSocket.listen(50)
        print("服务器已启动")
        while True:
            # 连接并启动线程
            clientSocket, addr = self.serverSocket.accept()
            print("新连接", addr)
            threading.Thread(target=self.handle, args=(clientSocket,)).start()


    # 这个方法用于处理玩家刚连接时到进入房间的过程
    # 开新线程是为了不阻塞主线程
    def handle(self, clientSocket: socket.socket) -> None:
        while True:
            # 连接成功后输入房间号和用户名
            message = socket_recv(clientSocket)
            if message.type == 'roomAndName':
                room_id = message.content[0]
                username = message.content[1]
                print("用户", username, "请求进入房间", room_id)
            else:
                continue

            # 下面的操作涉及共享资源 需要加锁
            with self.lock:
                # 如果房间号不存在则创建房间
                if room_id not in self.room:
                    self.room[room_id] = Room()
                    threading.Thread(target=self.room[room_id].work).start()
                    self.room[room_id].add_player(clientSocket, username)
                    print("用户", username, "成功进入房间", room_id)
                    break
                # 如果房间号存在 则先判断房间是否已满 再判断名字是否重复
                else:
                    if self.room[room_id].is_full:
                        clientSocket.send(Message('reroom_id', -1).serialize())
                        print("用户", username, "请求进入的房间", room_id, "已满")
                        continue
                    elif username in self.room[room_id].usernames.values():
                        clientSocket.send(Message('rename', -1).serialize())
                        print("用户", username, "请求进入的房间", room_id, "用户名重复")
                        continue
                    else:
                        self.room[room_id].add_player(clientSocket, username)
                        print("用户", username, "成功进入房间", room_id)
                        break
        # 剩下的逻辑交给room处理 server不用管了
        return

if __name__ == '__main__':
    server = Server()
    server.start()