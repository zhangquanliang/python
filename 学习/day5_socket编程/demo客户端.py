# -*- coding: utf-8 -*-
import socket

# 创建 socket 对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# host = socket.gethostname()
port = 9999
host = '127.0.0.1'

# 连接服务，指定主机和端口
s.connect_ex((host, port))

# 接收小于 1024 字节的数据
msg = s.recv(1024)

s.close()

print(msg.decode('utf-8'))