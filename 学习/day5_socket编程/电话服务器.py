# -*- coding: utf-8 -*-
#  Author: zhangql
import socket
import subprocess

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # 绑定协议，生成套接字
ip_port = ('127.0.0.1', 222)
s.bind(ip_port)   # 绑定ip+协议+端口：用来唯一标识一个进程，ip_port必须是元组格式
s.listen(5)   # 定义最大可以挂起链接数

# 等待电话
while True:
    c, addr = s.accept()  # 接收客户端请求，返回conn（相当于一个特定胡链接），addr是客户端ip+port
    c.sendall(bytes('欢迎致电 10086，请输入1xxx,0转人工服务.',encoding='utf-8'))

    # 接消息
    while True:  # 用来基于一个链接重复收发消息
        try:  # 捕捉客户端异常关闭（ctrl+c）
            recv_data = s.recv(1024)  # 收消息，阻塞

            if len(recv_data) == 0: break  # 客户端如果退出，服务端将收到空消息，退出
            # 执行系统命令，windows平台命令的标准输出是gbk编码，需要转换
            # 发消息
            p = subprocess.Popen(str(recv_data, encoding='utf8'), shell=True, stdout=subprocess.PIPE)
            res = p.stdout.read()  # 标准输出
            print('11111111', res)
            if len(res) == 0:   # 执行错误命令，标准输出为空，
                send_message = 'cmd err'
            else:
                print('1111')

                send_message = bytes(str(res.encode('utf8'), encoding='utf8'))

            # 解决粘包问题
            # ready_tag = 'Ready|%s' % len(send_message)
            # c.send(bytes(ready_tag, encoding='utf8'))  # 发送数据长度
            # feedback = c.recv(1024)  # 接收确认信息
            # feedback = str(feedback, encoding='utf8')
            #
            # if feedback.startswith('Start'):
            #     c.send(send_message)  # 发送命令的执行结果
            c.send(send_message)
        except:
            break
    c.close()