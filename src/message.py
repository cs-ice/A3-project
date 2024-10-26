from collections import defaultdict, deque
import socket
import threading
import json

'''
为了数据传输能够正确运行 我们除了message类之外还需要定义一些规则
那就是消息头机制
在发送消息的时候 我们需要在message的前面加上一个4字节的消息头 用来表示message的长度
所以我们发送的二进制流格式如下
消息头(4字节) + 消息体(长度不定)

服务端发送给客户端的消息类型以及内容需要按下面的格式打包
1."id"              content为int        客户端的id(int)
2."rename"          content无意义       名字重复 用-1代替
3."reroom_id"       content无意义       重新输入房间号 用-1代替
4."wait"            content无意义       用-1代替
5."new_player"      content为lst        [id(int)以及名字(str)]
6."ready_lst"       content为lst        已准备的玩家列表[id(int)]
7."handcard"        content为lst        手牌列表[int]
8."start"           content无意义       用-1代替
9."curr"            content为lst        当前出牌的信息[当前有出牌权的玩家(int) 上一个出牌权的人出的牌(lst)]
10."over"           content为lst        [该客户端是否胜利[bool] 所有玩家得分结果[int]]

客户端发送给服务端的消息需要按下面的格式打包
1."roomAndName"     content为lst        [房间号(int) 用户名(str)]        
2."ready"           content为bool       发送一个content为true的信号 表示准备
3."play"            content为lst        客户端打出的牌 为int的列表
4."chat"            content为str        客户端发送的信息



'''



# 消息类
class Message:
    def __init__(self, type:str, content:any):
        self.type = type
        self.content = content

    # 序列化成含有消息头的二进制流
    def serialize(self) -> bytes:
        # 利用jasn以及__dict__将对象序列化为json字符串
        # __dict__是一个包含对象属性的字典
        jsonstr = json.dumps(self.__dict__).encode('utf-8')
        # 返回消息头+消息体
        length_bytes = len(jsonstr).to_bytes(4, byteorder='big')
        return length_bytes + jsonstr        
    
    
    # 反序列化 但是这里的反序列化不能解析出消息头 所以需要在外部解析
    @classmethod
    def deserialize(cls, byte_stream: bytes)-> 'Message':
        try:
            json_data = byte_stream.decode('utf-8')
            data = json.loads(json_data)
            return cls(data['type'], data['content'])
        except (ValueError, KeyError, TypeError) as e:
            # 捕获 JSON 解析错误或数据不全的情况
            print(f"Failed to deserialize message: {e}")
            return None


# 封装好socket接收含有消息头的二进制流
def socket_recv(socket: socket.socket) -> Message:
    length_bytes = socket.recv(4)
    if len(length_bytes) < 4:
        return None
    length = int.from_bytes(length_bytes, byteorder='big')
    data = b''
    while len(data) < length:# while保证接收到完整的数据
        part = socket.recv(length - len(data))
        if not part:
            break
        data += part
    return Message.deserialize(data)

# 消息池类
class MessagePool:
    def __init__(self):
        self.broadcast_message = deque()                # 广播消息池
        self.client_message = defaultdict(deque)        # 客户端消息池(dfdict是一个有默认值的字典)
        self.lock = threading.Lock()                    # 锁保证线程安全
    
    # 添加广播消息
    def add_broadcast_message(self, message: Message) -> None:
        with self.lock:
            self.broadcast_message.append(message)

    # 添加点对点消息
    def add_client_message(self, id: int, message: Message) -> None:
        with self.lock:
            self.client_message[id].append(message)
        
    # 获取下一个广播消息
    def get_next_broadcast_message(self) -> Message:
        with self.lock:
            return self.broadcast_message.popleft() if self.broadcast_message else None
    
    def get_next_client_message(self, id: int) -> Message:
        with self.lock:
            return self.client_message[id].popleft() if self.client_message[id] else None
    
    # 判断是否有广播消息
    def has_broadcast_message(self) -> bool:
        with self.lock:
            return len(self.broadcast_message) > 0
        
    # 判断是否有点对点消息
    def has_client_message(self, id: int) -> bool:
        with self.lock:
            return len(self.client_message[id]) > 0