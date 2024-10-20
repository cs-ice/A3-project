import socket

# 地址族为IPv6，套接字类型为TCP
# 这个套接字用来连接服务器
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 整了一个阿里云服务器
serverIP = "8.217.57.241"
serverPort = 12345

# 连接服务器
clientSocket.connect((serverIP, serverPort))

# 发送数据给服务器
message = input("Please enter something: ")
clientSocket.send(message.encode())

# 接收服务器发送的数据
data = clientSocket.recv(1024)
print("Received:", data.decode())