# -*- coding: utf-8 -*-
"""
Title = 邮件发送
Date = 20180402
"""
# coding=utf-8
import smtplib
from email.mime.text import MIMEText

msg_from = '1007228376@qq.com'  # 发送方邮箱
passwd = 'midanhjvoecubfid'  # 填入发送方邮箱的授权码
# msg_to = 'zhangql@legion-tech.net, 1607228376@qq.com'  # 收件人邮箱
msg_to = '1607228376@qq.com'  # 收件人邮箱

subject = "python邮件测试"  # 主题
content = "python多人发送测试"  # 内容
msg = MIMEText(content)
msg['Subject'] = subject
msg['From'] = msg_from
msg['To'] = msg_to
try:
    # 连接smtp服务器，明文/SSL/TLS三种方式，根据你使用的SMTP支持情况选择一种
    # 普通方式，通信过程不加密 仅限本地用户
    # s = smtplib.SMTP("smtp.qq.com", "25")  # 默认为端口25
    # s.ehlo()
    # s.login(msg_from, passwd)

    # tls加密方式，通信过程加密，邮件数据安全，使用正常的smtp端口
    # s = smtplib.SMTP("smtp.qq.com", "25")
    # s.set_debuglevel(True)
    # s.ehlo()
    # s.starttls()
    # s.ehlo()
    # s.login(msg_from, passwd)

    # 纯粹的ssl加密方式，通信过程加密，邮件数据安全
    s = smtplib.SMTP_SSL("smtp.qq.com", 465)  # SSL端口465 邮件服务器及端口号
    s.login(msg_from, passwd)

    # 发送邮件
    s.sendmail(msg_from, msg_to, msg.as_string())
    # s.close()
    print("发送成功")
except Exception as error:
    print('发送异常', error)
finally:
    s.quit()