import socket

class Client:

    # 初始化客户端套接字
    def __init__(self):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 连接服务器
    def connect(self):
        serverIP = "8.217.57.241"
        serverPort = 12345
        self.clientSocket.connect((serverIP, serverPort))
    
    # 发送数据给服务器
    def send(self, message):
        self.clientSocket.send(message.encode())