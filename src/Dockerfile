# 使用官方 Python 镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 复制当前目录的所有文件到容器中的 /app 目录
COPY . .

# 安装依赖（如果有需要的话，添加 requirements.txt）
# RUN pip install -r requirements.txt

# 暴露服务端口
EXPOSE 12345

# 运行服务端程序
CMD python3 server.py
