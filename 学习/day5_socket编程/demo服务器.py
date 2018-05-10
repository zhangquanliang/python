# -*- coding: utf-8 -*-
import socket

# 创建 socket 对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 获取主机名
# host = socket.gethostname()
port = 9999
host = '127.0.0.1'

# 绑定端口号
s.bind((host, port))

# 设置最大连接数
s.listen(5)

while True:
    # 建立客户端连接
    c, addr = s.accept()
    print(c)
    print('连接地址为: %s' % str(addr))
    msg = '欢迎来到张全亮的socket示例!'
    c.send(msg.encode('utf-8'))
    c.close()
