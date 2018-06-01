# -*- coding:utf-8 -*-
"""
author = zhangql
"""
import socket
sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sk.connect(('zhangql', 2222))

data = sk.recv(1024)
sk.close()
print(data.decode())