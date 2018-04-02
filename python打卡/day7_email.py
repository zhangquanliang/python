# -*- coding: utf-8 -*-
"""
Title = 发送邮件(带附件)
Date = 20180402
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


class QQEmail:
    def __init__(self):
        self.smt_obj = smtplib.SMTP_SSL('smtp.qq.com', 465)   # host=smtp.qq.com , post=465
        self.msg_from = '1007228376@qq.com'  # 发送邮箱
        self.msg_to = '1607228376@qq.com, 3429275949@qq.com'    # 接受邮箱
        self.password = 'midanhjvoecubfid'  # 发送方邮箱的授权码

    def send_email(self):
        subject = "这是一个带附件的打开任务"   # 主题
        message_context = "hello，我是打卡小程序的任务"
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = self.msg_from
        msg['To'] = self.msg_to
        msg.attach(MIMEText(message_context, 'plain', 'utf-8'))

        # txt附件
        att1 = MIMEApplication(open('fans_list.txt', 'rb').read())
        att1.add_header('Content-Disposition', 'attachment', filename='TXT附件.txt')
        msg.attach(att1)

        # pdf附件
        att2 = MIMEApplication(open('688152326_20180318.pdf', 'rb').read())
        att2.add_header('Content-Disposition', 'attachment', filename='PDF附件.pdf')
        msg.attach(att2)

        # xlsx类型的附件
        att3 = MIMEApplication(open('张全亮10月加班记录.xlsx', 'rb').read())
        att3.add_header('Content-Disposition', 'attachment', filename='XLSX附件.xlsx')
        msg.attach(att3)

        # png类型的附件
        att4 = MIMEApplication(open('HX_verify_code.png', 'rb').read())
        att4.add_header('Content-Disposition', 'attachment', filename='PNG附件.jpg')
        msg.attach(att4)

        # mp3类型的附件
        # mp3part = MIMEApplication(open('kenny.mp3', 'rb').read())
        # mp3part.add_header('Content-Disposition', 'attachment', filename='benny.mp3')
        # msg.attach(mp3part)

        try:
            self.smt_obj.login(self.msg_from, self.password)
            self.smt_obj.sendmail(self.msg_from, self.msg_to, msg.as_string())
            print('用户{}发送给用户{}邮件成功'.format(self.msg_from, self.msg_to))
        except Exception as error:
            print('发送邮件异常', error)
        finally:
            self.smt_obj.close()


if __name__ == '__main__':
    qq_email = QQEmail()
    qq_email.send_email()