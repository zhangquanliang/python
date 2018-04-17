# -*- coding: utf-8 -*-
"""
通过smtplib.SMTP_SS发送邮件信息
"""
# coding=utf-8
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

msg_from = '1007228376@qq.com'  # 发送方邮箱
passwd = 'midanhjvoecubfid'  # 填入发送方邮箱的授权码
msg_to = '1607228376@qq.com'  # 收件人邮箱

subject = "python邮件测试"  # 主题
content = "python多人发送测试"  # 内容

# 创建一个带附件的实例
msg = MIMEMultipart()
msg['Subject'] = subject
msg['From'] = msg_from
msg['To'] = msg_to
msg.attach(MIMEText('这是菜鸟教程Python 邮件发送测试……', 'plain', 'utf-8'))  # 发送的内容

# 构造附件1，传送当前目录下的 test.txt 文件
att1 = MIMEText(open('fans_list.txt', 'rb').read(), 'base64', 'utf-8')
att1["Content-Type"] = 'application/octet-stream'
# 这里的filename可以任意写，写什么名字，邮件中显示什么名字
att1["Content-Disposition"] = 'attachment; filename=%s' % ('粉丝.txt'.encode('gb2312'))
msg.attach(att1)
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