# -*- coding:utf-8 -*-
"""
author = zhangql
"""
import socket

sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'zhangql'
port = 2222
sk.bind((host, port))
sk.listen(5)
while True:
    try:
        c, addr = sk.accept()
        message = '欢迎'
        print('连接地址为: %s' % str(addr))
        c.send(message.encode('utf-8'))
        c.close()
    except:
        pass