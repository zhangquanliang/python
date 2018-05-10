# -*- coding: utf-8 -*-
import requests
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 36))

msg = s.recv(1024)
print(msg.decode())
s.close()
