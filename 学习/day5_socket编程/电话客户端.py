# -*- coding: utf-8 -*-
#  Author: zhangql
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # 绑定协议，生成套接字
ip_port = ('127.0.0.1', 222)
s.connect(ip_port)  # 链接服务端，如果服务已经存在一个好的连接，那么挂起

welcom_msg = s.recv(200).decode()  # 获取服务端欢迎消息
print(welcom_msg)
while True:
    msg_size = 0
    send_message = input(">>:").strip()
    if send_message == 'exit': break
    if len(send_message) == 0: continue
    s.send(bytes(send_message, encoding='utf8'))
    msg = s.recv(1024)
    print(msg)
    # # 解决粘包问题
    # ready_tag = s.recv(1024)  # 收取带数据长度的字节：Ready|9998
    # print(ready_tag)
    # ready_tag = str(ready_tag, encoding='utf8')
    # if ready_tag.startswith('Ready'):  # Ready|9998
    #     msg_size = int(ready_tag.split('|')[-1])  # 获取待接收数据长度
    # start_tag = 'Start'
    # s.send(bytes(start_tag, encoding='utf8'))  # 发送确认信息

    # 基于已经收到的待接收数据长度，循环接收数据
    # recv_size = 0
    # recv_msg = b""
    # while recv_size < msg_size:
    #     recv_data = s.recv(1024)
    #     recv_msg += recv_data
    #     recv_size += len(recv_data)
    #     print('MSG SIZE %s RECE SIZE %s' % (msg_size,recv_size))
    # print(str(recv_msg,encoding='utf8'))
s.close()