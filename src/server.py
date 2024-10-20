import socket


# 地址族为IPv4，套接字类型为TCP
# 这个套接字用来监听客户端的连接请求
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定IP地址和端口号
serverSocket.bind(('0.0.0.0', 12345))

# 开始监听，最大连接数为5
serverSocket.listen(5)
print("Server is listening...")

while True:
    # 接受客户端的连接请求
    clientSocket, clientAddr = serverSocket.accept()
    print("Connection from", clientAddr)

    # 接收客户端发送的数据
    revmessage = clientSocket.recv(1024).decode()
    print("Received:", revmessage)

    # 发送数据给客户端
    sendmessage = "Hello, I'm server." + "here is your upper case: " + revmessage.upper()
    clientSocket.send(sendmessage.encode())

    # 关闭客户端套接字
    clientSocket.close()

